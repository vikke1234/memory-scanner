#ifndef __x86_64__
#warning                                                                       \
    "this program might not work as intended on other architectures than x64 due to some UB"
#endif

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/uio.h>
#include <unistd.h>

#include "memory.h"

/**
   this is just to easily asses the size of a union
*/
size_t type_to_size[] = {[UINT8] = sizeof(uint8_t),
                         [UINT16] = sizeof(uint16_t),
                         [UINT32] = sizeof(uint32_t),
                         [UINT64] = sizeof(uint64_t)};

bool compare_value(struct value_t *v1, struct value_t *v2) {
  if (v1 == NULL || v2 == NULL) {
    return false;
  }
  if (v1->type != v2->type) {
    return false;
  }
  switch (v1->type) {
  case UINT8:
    return v1->value.u8 == v2->value.u8;
  case UINT16:
    return v1->value.u16 == v2->value.u16;
  case UINT32:
    return v1->value.u32 == v2->value.u32;
  case UINT64:
    return v1->value.u64 == v2->value.u64;
  default:
    return false;
  }
}

/**
   @param pid the pid of the process
   @param addr the address to read from
   @param buffer the buffer to store the value into
   @param size the size of the buffer (also read this many bytes from addr)
   @return returns bytes read (return value of process_vm_readv)
*/
extern ssize_t read_process_memory(const pid_t pid, void *const addr,
                                   char *const buffer, size_t size) {
  const long PAGE_SIZE = sysconf(_SC_PAGESIZE);
  const long IOVEC_MAX = sysconf(_SC_IOV_MAX);
  const int amount_of_iovecs = size / PAGE_SIZE ? size / PAGE_SIZE : 1;

  /* used to keep track of how many iovecs still need to be made */
  size_t size_copy = size;
  struct iovec *remotes = malloc(sizeof(struct iovec) * amount_of_iovecs);
  struct iovec local = {buffer, size};

  if (size > PAGE_SIZE) {
    int i = 0;
    /*
      NOTE: This is taken from the `process_vm_readv` manpage, because of this
      I've made it split it up accordingly.

      Keep  this  in  mind  when  attempting to read data of unknown
      length (such as C strings  that  are  null-terminated)  from  a  remote
      process,  by avoiding spanning memory pages (typically 4 KiB) in a sin‐
      gle remote iovec element.  (Instead, split the remote read into two re‐
      mote_iov  elements  and  have  them  merge back into a single write lo‐
      cal_iov entry.  The first read entry goes  up  to  the  page  boundary,
      while the second starts on the next page boundary.)

     */
    do {
      remotes[i].iov_base = addr + i * PAGE_SIZE;
      remotes[i].iov_len = PAGE_SIZE;
      i++;
      size_copy -= PAGE_SIZE;
    } while (size_copy >= PAGE_SIZE);

    if (size_copy > 0) {
      remotes[i].iov_base = addr + i * PAGE_SIZE;
      remotes[i].iov_len = size_copy;
    }
  } else {
    remotes->iov_base = addr;
    remotes->iov_len = size;
  }
  size_t bytes_read =
      process_vm_readv(pid, &local, 1, remotes, amount_of_iovecs, 0);
  free(remotes);
  return bytes_read;
}

extern ssize_t write_process_memory(const pid_t pid, void *const addr,
                                    const uint8_t *const buffer,
                                    const size_t size) {
  return 0;
}

/**
   scans the memory of a process
   @details this could probably have some sort of settings thing so you could
   choose to look for aligned/non aligned variables, for now it only looks for
   aligned ones

   @param pid the pid of the process
   @param start the starting address from where to search
   @param the length of addresses to search
   @param the value to look for

   @returns a pointer to a vector of entries (a skip list if you will )
*/
extern struct entry_list_t *scan_new(pid_t pid, void *start, size_t length,
                                     struct value_t search_for) {
  struct entry_list_t *list = malloc(sizeof(struct entry_list_t));
  /*
    just an arbitrary number, didn't think too much of it,
    with some statistics it could probably be made better
  */
  const size_t INITIAL_LIST_SIZE = length / 4;
  const size_t size = type_to_size[search_for.type];

  struct entry_t entry = {0};
  entry.value.type = search_for.type;

  list->size = INITIAL_LIST_SIZE;
  list->capacity = 0;
  list->entries = calloc(INITIAL_LIST_SIZE, sizeof(struct entry_t *));

  for (size_t i = 0; i < length; i += size) {
    /* TODO: this may again be UB... mightfix */
    read_process_memory(pid, start + i, (char *)&entry.value.value, size);

    if (compare_value(&entry.value, &search_for)) {
      if (list->capacity == list->size) {
        size_t new_size = list->size * 3 / 2;
        struct entry_t **copy =
            realloc(list->entries, new_size * sizeof(struct entry_t *));
        /* TODO make sure this shit works */
        if (copy != NULL) {
          list->entries = copy;
          list->size = new_size;
        } else {
          perror("scan_new");
        }
      }
      entry.address = start + i;
      list->entries[list->capacity] = malloc(sizeof(struct entry_t));
      memcpy(list->entries[list->capacity], &entry, sizeof(struct entry_t));
      list->capacity++;
    }
  }
  return list;
}

extern void scan_old(pid_t pid, struct entry_list_t *entries,
                     struct value_t search_for) {
  if (entries == NULL) {
    return;
  }

  size_t *capacity = &entries->capacity;
  struct value_t current_value = {0};
  current_value.type = search_for.type;

  for (size_t i = 0; i < *capacity; i++) {
    if (entries->entries[i] == NULL) {
      /* this shouldn't happen but just there for safety */
      continue;
    }

    struct entry_t *entry = entries->entries[i];
    size_t size = type_to_size[entry->value.type];

    /* TODO: this might be UB, but it's nice and comfy at the moment */
    read_process_memory(pid, entry->address, (char *)&current_value.value,
                        size);

    if (!compare_value(&current_value, &search_for)) {
      free(entry);
      entries->entries[i] = NULL;
    } else {
      memcpy(&entry->value, &current_value, sizeof(struct value_t));
    }
  }
}
