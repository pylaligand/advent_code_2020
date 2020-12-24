# Day 23

Why two versions? First came a Python version without the doubly linked list,
with obvious performance issues on the second part. That version got turned into
the existing Rust version, with a few performance improvements which were
unfortunately not enough to solve the second part fast enough. Since
implementing linked lists in Rust is harder than PvNP, the Python version was
improved to rely on a custom linked list.
