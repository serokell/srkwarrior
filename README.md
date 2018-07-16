# Serokellwarrior

Integration with Bugwarrior, Taskwarrior and Timewarrior.

## Features

Export assigned YouTrack issues into local Taskwarrior DB:
```sh
$ bugwarrior-pull # Synchronize YouTrack with local DB
$ task # List tasks
$ task project:serokell.AD # List tasks in a project
```

Integrate Taskwarrior with Timewarrior for time tracking:
```sh
$ task /OPS-200/ start # Clock in
$ task /OPS-200/ stop # Clock out
```

Generate reports via `serokellwarrior-report` that can be annotated
with subitems:
```sh  
$ task /OPS-200/ annotate "Do this"
$ task /OPS-200/ annotate "Do that"
$ serokellwarrior-report
May 7:
 * OPS-200 Expose deployment info
   - Do this
   - Do that
```

Track time into YouTrack on `serokellwarrior-export`, very unlikely
to clock anything twice:
```sh
$ serokellwarrior-export
```

## Install

If you don't have Nix set up yet, run `curl https://nixos.org/nix/install | sh`.

Clone this repository, `cd` into it, run: `nix-env -if .`

You will also need to install Bugwarrior, Timewarrior, and Taskwarrior. Run: 

```sh
nix-env -f '<nixpkgs>' -iA python3Packages.bugwarrior taskwarrior timewarrior
```

## Setup

Run `task` and reply `y`.

Run `timew` and reply `y`.

Create `~/.config/bugwarrior/bugwarriorrc` that looks like this:

```
[general]
targets = serokell

[serokell]
service = youtrack
youtrack.description_template = [{{youtrackissue}}] {{youtracksummary}}
youtrack.project_template = serokell.{{youtrackproject}}
youtrack.host = issues.serokell.io
youtrack.login = <your login>
youtrack.password = <your password>
```

Usually, YouTrack accounts don't have login/password. To create
credentials, go to https://issues.serokell.io/users/me and click on "Update
personal information and manage logins". Then, press "Add credentials" and
enter login and password that you would like to use in the RC file above.

If you have any issues with that step (or anything regarding this program
whatsoever), don't hesitate to drop a line at #operations channel on Slack.

Pull YouTrack issues: `bugwarrior-pull`

If that works, there is one last step:

```sh
ln -s $(which serokellwarrior-hook) ~/.task/hooks/on-modify.serokellwarrior
```

Try clocking into some task and check if it's in `serokellwarrior-report`.

## Learn

For managing Serokell tasks, one will only need the following commands:

* `bugwarrior-pull` to sync with YouTrack
* `task` to list all assigned tasks
* `task /OPS-200/ start` to clock in
* `task /OPS-200/ stop` to clock out
* `task /OPS-200/ annotate "Message"` to add annotations
* `serokellwarrior-report` to generate a report for today,
  `serokellwarrior-report week` to generate a report for the last week,
  `serokellwarrior-report yesterday - today` to generate a report for yesterday
* `serokellwarrior-export` to export all clocked time that has not yet been exported

You might also find visual reports like `timew day` and `task burndown` useful.

If you want to learn more about Taskwarrior, here are some things you might
want to check out:

* [Taskwarrior start guide][taskwarrior-start-guide]
* ["Manage all your tasks with TaskWarrior"][taskwarrior-pjf-talk], talk by Paul Fenwick
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

Taskwarrior, on the other hand, is a DB-driven productivity tool, with a suite
of related programs like Timewarrior and Bugwarrior. Its design seems to have
significant improvements in our case, making it easier and more reliable to
query issues, track state changes (Taskwarrior is journaled), sync to a phone,
and integrate with other tools like our YouTrack.

Python is used for several reasons, the main one being that Bugwarrior is also
written in Python, so reusing its implementation saves a ton of work. Another
constraint is that the hook program has to start up very quickly (under .05s)
because it is run on every Taskwarrior change, so Elixir with its 0.3s startup
is not an option. It also seems to be preferable to have something that can
integrate with Nix easily without long build times.

## Developer documentation

* [Bugwarrior YouTrack module][bugwarrior-youtrack]
* `task(1)`, `timew(1)` man pages
* [YouTrack Work Item API][youtrack-work-item-api]

[bugwarrior-youtrack]: https://github.com/ralphbean/bugwarrior/blob/develop/bugwarrior/services/youtrack.py
[youtrack-work-item-api]: https://www.jetbrains.com/help/youtrack/standalone/Create-New-Work-Item.html

## Missing features

* Sending reports to Slack is currently not implemented. This is not urgent
  because Serokellwarrior is new and one is expected to eyeball reports before
  sending them to #team-updates channel. This feature will be added once report
  generation is proven to be reliable, though.
* Bugwarrior doesn't currently implement token-based authentication for
  YouTrack, so you will need to create a login/password pair. If you're not
  sure how, ask the operations team.
* `serokellwarrior-export` tool is not safe if anything else modifies
  Timewarrior DB while it runs. The problem here is that Timewarrior entries,
  unlike Taskwarrior, do not have UUIDs, only relative IDs. This can be
  resolved either by sending a patch to Timewarrior that adds UUIDs, or by
  locking the database while export tool runs (for example, by moving the
  directory to another place, and then moving it back, or sending patch to
  Timewarrior that makes it lock-aware).  This issue has high priority as it
  has potential to cause data loss.
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
