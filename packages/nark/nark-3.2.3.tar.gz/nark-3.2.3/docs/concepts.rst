########
Concepts
########

.. |nark| replace:: ``nark``
.. _nark: https://github.com/tallybark/nark

.. |hamster-lib| replace:: ``hamster-lib``
.. _hamster-lib: https://github.com/projecthamster/hamster-lib

This is a high-level, very general overview of basic |nark|_ concepts.

(These concepts are essentially the same as those in
`Legacy Hamster <https://github.com/projecthamster/hamster>`__,
as well as in the stalled |hamster-lib|_ project.)

Fact
   The essence of |nark|_ is the *Fact*, an interval of time having a start
   time and almost always having an end time (except for the *active Fact*).
   A Fact may also be associated with a specific *Activity*,
   which itself is associated with a specific *Category*.
   Facts may have zero or more *Tags* assigned to them.
   Also, a Fact has a *Description*.

   No two Facts may occupy the same *time window*,
   i.e., the start-to-end times of two separate Facts may not overlap.

Factoid
   A *Factoid* is a string representation of a Fact. It can be parsed
   to create a new Fact instance, and it can contain any of:
   a start time, an end time, an activity, a category, zero or more tags,
   and a Fact description.

Activity
   An *Activity* generally describes what occurred during the time
   interval captured by the Fact.

   For instance, the user might choose to use "Meeting" and
   "Coffee break", among other names, for their Activities.

Category
   A *Category* describes a collection of Activities.

   Categories allow the user to reuse the same Activity name (by using
   different Category names). Also, Categories allow the user to group
   Activities, which could be useful for reporting and other features.

   For instance, the user might choose to use "Work" and "Personal",
   among other names, for their Activities' Categories.

Act\@Gory
   An *Act@Gory* (pronounced "act-eh-gory") is a documentation construct
   for the combined Activity and Category names for a given Fact. It is
   so-called because the ``dob`` CLI parser expects the user to specify
   the activity with the *at* (``@``) symbol.
   For instance, in the following Factoid,
   ``at 08:00: Meeting@Work: I wish I was outside.``,
   the Act\@Gory is ``Meeting@Work`` (where ``Meeting`` is
   the Activity and ``Work`` is the Category, naturally).

Tag
   A *tag* is another way to label a Fact other than using an Act\@Gory.

   A tag is simply a string associated with a Fact.

   The user can apply more than one Tag to any Fact.

   Tags are not associated with any specific Activity or Category.

   - Though the user could, e.g., search for Facts and restrict to a
     specific Act\@Gory, and to a specific Tag, so there will be an
     inherent relationship between Tags and Activities simply by their
     association to the same Fact. But outside of Facts themselves,
     there is no relationship between Tags and Activities
     (nor between Tags and Categories).

Musings on Metadata
   *How do I, the user, know when to use an Activity or when to use a Tag?*

   Essentially, at its core, a Tag is the same construct as an Act\@Gory:
   It's simply a string associated with a Fact.

   As such, a decent end user application will, for instance, enable the user
   to search for Facts using Tag names just as easily as it will allow the
   user to search for Facts using Act\@Gory names.

   Really, what it boils down to is user preference.

   - Consider the user who works on a different project every day.

     Would the user prefer not to use tags, but to use a new Activity label everyday?
     Or would the user prefer to use the same Activity label every day, but to specify
     a new Tag name every day instead?

     *The answer:* It's up to the user! Either approach works fine.
     But the application experience will be slightly different
     between the two approaches.

Active Fact
   An *active* Fact has no end time, and its start time is
   at or after all other Facts' end times.

   There can be at most one active Fact in the data store, and,
   if it exists, it is the latest Fact chronologically.

   - In Legacy Hamster, the user could save any Fact without an end time.
     And sometimes the application did so by accident (*read: bug*).
     But having more than one unclosed Fact wreaks havoc when trying to do
     interesting things with the data, such as generating reports, or compiling
     statistics. As such, |nark|_ imposes a limit of one such open-ended Fact.
     Also, when upgrading a legacy database, |nark|_ will close any open Facts
     it finds (making them *momentaneous* Facts instead).

     - An active Fact might also be considered *endless* or *ongoing*,
       but an endless or ongoing Fact is not necessarily the active Fact.
       An endless or ongoing Fact simply does not have an end time, and
       in legacy Hamster, there could be many of these.

   - In stalled |hamster-lib|_, the active Fact was instead called the
     *temporary fact*, or *tmp_fact*, and it was pickled and saved to a file
     on the file system, rather than stored in the database alongside other
     Facts. We shall speak of this imprudence no further.

Momentaneous Fact
   A *momentaneous* Fact is a Fact whose start time is the same as its end time.

   Such a feature may seem a bit contrived, but it's necessary to handle some
   bugs in Legacy Hamster. It also allows the user to make multiple Facts at
   the same time without violating the no-2-Facts-may-overlap rule, which could
   be a handy trick for creating different Facts at the same time, but using
   different Act\@Gories and Tags.

