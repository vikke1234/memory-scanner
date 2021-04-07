#ifndef MEMORY_H
#define MEMORY_H
#include <stdint.h>

extern ssize_t read_process_memory(const pid_t pid, void *const addr,
                                   char *const buffer, size_t size);

extern ssize_t write_process_memory(const pid_t pid, void *const addr,
                                    const char *const buffer,
                                    const size_t size);
#endif /* MEMORY_H */
