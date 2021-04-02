#ifndef MEMORY_H
#define MEMORY_H
#include <bits/stdint-uintn.h>
#include <stdint.h>
#include <stdlib.h>

enum type_t { UINT8, UINT16, UINT32, UINT64 };

struct value_t {
  enum type_t type;
  union value_union_t {
    uint8_t u8;
    uint16_t u16;
    uint32_t u32;
    uint64_t u64;
  } value;
};

struct entry_t {
  void *address;
  struct value_t value;
};

/**
   this is a skiplist, it places NULLs at the indexes where it doesn't find a
   value then it swaps the deleted element with the last one in the array
 */
struct entry_list_t {
  /**
   size of the array
  */
  size_t size;
  /**
   amount of elements the array contains
  */
  size_t capacity;
  struct entry_t **entries;
};

extern ssize_t read_process_memory(const pid_t pid, void *const addr,
                                   char *const buffer, size_t size);

extern ssize_t write_process_memory(const pid_t pid, void *const addr,
                                    const uint8_t *const buffer,
                                    const size_t size);

extern struct entry_list_t *scan_new(pid_t pid, void *start, size_t length,
                                     struct value_t search_for);

extern void scan_old(pid_t pid, struct entry_list_t *entires,
                     struct value_t search_for);
#endif /* MEMORY_H */
