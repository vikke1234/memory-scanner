#ifndef __x86_64__
#warning                                                                       \
    "this program might not work as intended on other architectures than x64 due to some UB"
#endif

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <pybind11/pybind11.h>
#include <stdint.h>
#include <sys/mman.h>
#include <sys/uio.h>
#include "memory.h"

namespace py = pybind11;

/**
 *  Reads a processes memory at a given address
 *
 *  @param pid the pid of the process
 *  @param addr the address to read from
 *  @param buffer the buffer to store the value into
 *  @param size the size of the buffer (also read this many bytes from addr)
 *  @return returns bytes read (return value of process_vm_readv)
*/
extern ssize_t read_process_memory(const pid_t pid, void *const addr,
                                   char *const buffer, size_t size) {
    const long PAGE_SIZE = sysconf(_SC_PAGESIZE);
    const long IOVEC_MAX = sysconf(_SC_IOV_MAX);
    const int amount_of_iovecs = size / PAGE_SIZE ? size / PAGE_SIZE : 1;

    /* used to keep track of how many iovecs still need to be made */
    size_t size_copy = size;
    struct iovec *remotes = new struct iovec[amount_of_iovecs];
    struct iovec local = {buffer, size};

    if (size > PAGE_SIZE) [[unlikely]] {
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
            if (i >= IOVEC_MAX) {
                delete[] remotes;
                return -1;
            }
            remotes[i].iov_base = (char *) addr + i * PAGE_SIZE;
            remotes[i].iov_len = PAGE_SIZE;
            i++;
            size_copy -= PAGE_SIZE;
        } while (size_copy >= PAGE_SIZE);

        if (size_copy > 0) {
            remotes[i].iov_base = (char *) addr + i * PAGE_SIZE;
            remotes[i].iov_len = size_copy;
        }
    } else {
        remotes->iov_base = addr;
        remotes->iov_len = size;
    }
    size_t bytes_read =
            process_vm_readv(pid, &local, 1, remotes, amount_of_iovecs, 0);
    delete[] remotes;
    return bytes_read;
}

/**
 * writes to a given processes memory
 * @param pid       pid of the process
 * @param addr      address to write to
 * @param buffer    content that will be writtne
 * @param size      size of the buffer
 * @return          bytes written
 */
extern ssize_t write_process_memory(const pid_t pid, void *const addr,
                                    const char *const buffer,
                                    const size_t size) {

    return 0;
}

PYBIND11_MODULE(memory, m) {
    m.doc() = "Memory scanning extension";
    m.def("read_process_memory", &read_process_memory, py::arg("pid"), py::arg("addr"), py::arg("buffer"), py::arg("size"));
    m.def("write_process_memory", &write_process_memory, py::arg("pid"), py::arg("addr"), py::arg("buffer"), py::arg("size"));
}

