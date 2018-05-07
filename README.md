# Serokellwarrior

Integration with Bugwarrior, Taskwarrior and Timewarrior.

## Features

* Exports assigned YouTrack issues into local Taskwarrior DB
  (run `bugwarrior-pull` and then list tasks via `task ls`)
* Integrates Taskwarrior with Timewarrior so that when one types
  `task /OPS-200/ start` (or `stop`) Timewarrior clocks in/out
* Generates reports via `serokellwarrior-report` that can be annotated
  with subitems via `task /OPS-200/ annotate "Do this and that"`
* Tracks time into YouTrack on `serokellwarrior-export`, very unlikely
  to clock anything twice

## Install

Checkout and `cd` to this repository, and run `nix-env -if .`.

You will also need to install Bugwarrior, Timewarrior, and Taskwarrior. Run: 

```
nix-env -f '<nixpkgs>' -iA python3Packages.bugwarrior taskwarrior timewarrior
```

## Setup

TODO.

## Learn

For managing Serokell tasks, one will only need to know the following commands:

* `bugwarrior-pull` to sync with YouTrack
* `task` to list all assigned tasks
* `task /OPS-200/ start` to clock in
* `task /OPS-200/ stop` to clock out
* `serokell-report` to generate a report for today,
  `serokell-report week` to generate a report for the last week,
  `serokell-report yesterday - today` to generate a report for yesterday
* `serokell-export` to export all clocked time that has not yet been exported

You might also find visual reports like `timew day` and `task burndown` useful.

If you want to learn more about Taskwarrior, here are some things you might
want to check out:

* [Taskwarrior start guide][taskwarrior-start-guide]
* ["Manage all your tasks with TaskWarrior", talk by Paul Fenwick][taskwarrior-pjf-talk]
* Android version on [Google Play][taskwarrior-gplay] and [F-Droid][taskwarrior-fdroid]

[taskwarrior-fdroid]: https://f-droid.org/en/packages/kvj.taskw/
[taskwarrior-gplay]: https://play.google.com/store/apps/details?id=com.taskwc2
[taskwarrior-pjf-talk]: https://www.youtube.com/watch?v=zl68asL9jZA
[taskwarrior-start-guide]: https://taskwarrior.org/docs/start.html

## Rationale

Org mode, while convenient, is problematic due to its reliance on plain text.
This causes considerable issues when using Org mode on more than one device
(merge conflicts) and difficulties with manipulating/exporting/importing data,
any integration ultimately has to be done via custom inefficient parsers.

Taskwarrior, on the other hand, is a database-driven productivity tool, with a
suite of related programs like Timewarrior and Bugwarrior. It's very easy to
write programs that manipulate Taskwarrior, because it has JSON export.  That is
mainly why there we can pull off reliable sync from YouTrack to local DB, which
tracks issues not by their name or issue number but by UUID.

Data-driven design seems to have significant improvements in this case, making
it easier and more reliable to query issues, track state changes (Taskwarrior is
journaled), sync to a phone, and integrate with other tools.

Python is used for several reasons: the main one being that Bugwarrior is also
written in Python, so reusing its configuration file parser saves a lot of work,
and there's `taskw` pip package maintained by upstream that this program might
switch to. Other constraints are that those programs have to start up very
quickly (under .05s) because they are supposed to hook to Taskwarrior commands,
and preferably have something that can integrate into NixOS easily without long
build times.

## Developer documentation

* YouTrack time tracking API:
  https://www.jetbrains.com/help/youtrack/standalone/Create-New-Work-Item.html
* Bugwarrior YouTrack module:
  https://github.com/ralphbean/bugwarrior/blob/develop/bugwarrior/services/youtrack.py
* `task(1)`, `timew(1)` man pages

## Missing features

* Sending reports to Slack is currently not automated. This is not urgent
  because Serokellwarrior is new and one is expected to eyeball reports before
  sending them to #team-updates channel. This feature will be added once report
  generation is proven to be reliable, though.
* Bugwarrior doesn't currently implement token-based authentication for
  YouTrack, so you will need to create a username/password pair. If you're not
  sure how, ask the ops team.
* `serokellwarrior-export` tool is not safe if anything else modifies
  Timewarrior DB while it runs. The problem here is that Timewarrior entries,
  unlike Taskwarrior, do not have UUIDs, only relative IDs. This can be resolved
  either by sending a patch to Timewarrior that adds UUIDs, or by locking the
  database while export tool runs (for example, by moving the directory to
  another place, and then moving it back, or sending patch to Timewarrior that
  makes it lock-aware).  This issue has high priority as it has potential to
  cause data loss.
* `serokellwarrior-report` tool presumes that days are the smallest report
  granularity for annotations. It means that if you generate a report that is
  supposed to only include the last 4 hours of work, it will also include
  annotations for the rest of the day. Fixing this would mean reimplementing
  Timewarrior's interval parser, so unlikely to happen. People who send reports
  only once a day are not affected :-)

## Distribution

This package is supposed to be private, so that we don't leak the way Serokell
handles time tracking, reports and such to the world. This package is unlikely
to be of much use to anyone outside of the company anyway.
