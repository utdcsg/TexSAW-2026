# SIGBOVIK II - Errata Writeup

The fixed errata is that the PRIMAPPLY assembly instruction now accepts a program address as input, rather than a mnemonic.
This is discoverable by diffing the provided assembler source.
PRIMAPPLY needs a NULL in place, figure this out by compiling some scrop scheme.
So, pass in assembly source that looks like:

```
Load NULL
PRIMAPPLY <addr of win>
DONE
```

This prints out the flag
