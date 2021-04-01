#ifndef __x86_64__
#warning                                                                       \
    "this program might not work as intended on other architectures than x64 due to some UB"
#endif

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <bits/types/struct_iovec.h>
#include <python3.9/modsupport.h>
#include <python3.9/object.h>
#include <python3.9/Python.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/uio.h>
#include <unistd.h>
#include <stdbool.h>

#include "memory.h"

/**
   this is just to easily asses the size of a union
*/
size_t type_to_size[] = {[UINT8] = sizeof(uint8_t), [UINT16] = sizeof(uint16_t), [UINT32] = sizeof(uint32_t), [UINT64] = sizeof(uint64_t)};

bool compare_value(struct value_t *v1, struct value_t *v2) {
  if (v1 != NULL || v2 != NULL) {
    return false;
  }
  if (v1->type != v2->type) {
    return false;
  }
  switch(v1->type) {
  case UINT8:
    return v1->value.u8 == v2->value.u8;
  case UINT16:
    return v1->value.u16 == v2->value.u16;
  case UINT32:
    return v1->value.u32 == v2->value.u32;
  case UINT64:
    return v1->value.u64 == v2->value.u64;
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
      NOTE: This is taken from the `process_vm_readv` manpage, because of this I've made it split it up accordingly.

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
  return process_vm_readv(pid, &local, 1, remotes, amount_of_iovecs, 0);
}

extern ssize_t write_process_memory(const pid_t pid, void *const addr,
                                    const uint8_t *const buffer,
                                    const size_t size) {
  return 0;
}

extern struct entry_list *scan_new(pid_t pid, void *start, size_t length,
                                   struct value_t search_for) {
  return NULL;
}

extern struct entry_list *scan_old(pid_t pid, struct entry_list *entires,
                                   struct value_t search_for) {
  return NULL;
}
