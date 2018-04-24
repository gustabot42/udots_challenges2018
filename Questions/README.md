# Questions

1. How did you manage source control?

    * With github as a repository, git in command line
    and atom for easy visualization of files states.


2. What is the “single responsibility principle”? What's its purpose?

    * "Write programs that do one thing and do it well." -Unix philosophy
    * SRP means encapsulate the single meaningful functionality by artifact.
    * The purpose of SRP is maintainability of the integration by ensurance
    the qualities of the elements and their interactions.


3. What qualities should a “clean code” have?

    * Readability
    * Use the right tools for concepts encapsulation from variables to frameworks,
    each level have it purpose, each one have it ways to be named
    and it most to be descriptive
    * Testable, you can make better code if you are not worry to break it.


4. What is ACID?

    * Atomicity, Consistency, Isolation, Durability are a set of properties of database transactions.
    * Atomicity: all o nothing, if transactions fails roll back.
    * Consistency: there will be no degradation of the storage due to transactions.
    * Isolation: concurrency manipulation of data will be resolve as it was be sequentially.
    * Durability: once the transaction is finished, it will last.


5. What is the CAP Theorem?

    * Consistency, Availability, Partition tolerance are a tringle in witch
    a distribute data store can only select two.
    * Consistency: every user see the same data at the same time.
    * Availability: the system always have an answer even if it is not updated.
    * Partition tolerance: the system can works even
    if there is not good communication between its parts
