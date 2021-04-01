#include "memory.h"

extern ssize_t read_process_memory(const pid_t pid, void *const addr,
                                   char *const buffer, size_t size) {
  return 0;
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
