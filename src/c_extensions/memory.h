#ifndef MEMORY_H
#define MEMORY_H
#include <bits/stdint-uintn.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/queue.h>

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

struct search_result_t {
  struct value_t value;
  void *address;
  LIST_ENTRY(search_result_t) next;
};

LIST_HEAD(entry_list, search_result_t);

extern ssize_t read_process_memory(const pid_t pid, void *const addr,
                                   char *const buffer, size_t size);

extern ssize_t write_process_memory(const pid_t pid, void *const addr,
                                    const uint8_t *const buffer,
                                    const size_t size);

extern struct entry_list *scan_new(pid_t pid, void *start, size_t length,
                            struct value_t search_for);

extern struct entry_list *scan_old(pid_t pid, struct entry_list *entires,
                                   struct value_t search_for);
#endif /* MEMORY_H */
