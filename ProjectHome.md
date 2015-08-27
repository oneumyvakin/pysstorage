Structured Storage provides file and data persistence in COM by handling a single file as a structured collection of objects known as storages and streams.

The purpose of Structured Storage is to reduce the performance penalties and overhead associated with storing separate objects in a single file. Structured Storage provides a solution by defining how to handle a single file entity as a structured collection of two types of objects—storages and streams—through a standard implementation called Compound Files. This enables the user to interact with, and manage, a compound file as if it were a single file rather than a nested hierarchy of separate objects.

Structured Storage can be used on Microsoft COM-based operating systems.Besides having been the bread and butter for the Microsoft Office suite of applications for many years and almost all OLE applications that are capable of linking and embedding.

PySStorage is a pure python library to read/write Structured Storage files in COM

It follow the [MS-CFB](http://msdn.microsoft.com/en-us/library/cc546605.aspx) Compound File Binary File Format Specification