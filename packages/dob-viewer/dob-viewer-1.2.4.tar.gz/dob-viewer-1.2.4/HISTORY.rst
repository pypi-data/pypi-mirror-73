#######
History
#######

.. |dob| replace:: ``dob``
.. _dob: https://github.com/tallybark/dob

.. |dob-prompt| replace:: ``dob-prompt``
.. _dob-prompt: https://github.com/tallybark/dob-prompt

.. |dob-viewer| replace:: ``dob-viewer``
.. _dob-viewer: https://github.com/tallybark/dob-viewer

.. :changelog:

1.2.4 (2020-06-29)
==================

- Change ownership to https://github.com/tallybark.

1.2.3 (2020-06-18)
==================

- Packaging: Update dependency versions to pickup library changes.

1.2.2 (2020-06-18)
==================

- Bugfix: Catch overflow error when day delta too large.

  - E.g., if user enters jump command ``20200615J`` (when they meant
    to instead use the ``f`` command, not ``J``, i.e., ``20200615f``)
    catch and recover gracefully from the ``timedelta`` overflow error.

- Improve: Make mash-quit on unsaved changes prompt opt-in.

  - As a convenience to developers, mashing Ctrl-q would skip the
    save confirmation on exit; this feature is now opt in via the
    new config setting, ``dev.allow_mash_quit``.

- Packaging: Update dependencies.

- Update: General refactoring and updates per changes to other packages.

1.2.1 (2020-04-27)
==================

- Bugfix: Windows: Run ``notepad.exe`` if ``EDITOR`` not set.

  - Normally if ``EDITOR`` is not set, the system's ``sensible-editor``
    command will run Nano or Vi, neither of which is available on Windows.
    Consequently, on Windows, when ``EDITOR`` is not set, dob displays a
    warning, awaits acknowledgment, and then runs the Carousel again.

- Bugfix: Windows: Temporary file path broken because colon.

1.2.0 (2020-04-26)
==================

- Bugfix: Ensure warnings not cleared before awaiting acknowledgment.

1.1.2 (2020-04-25)
==================

- Bugfix: Part-specific styles not appearing until after focus.

  - Use case: Run ``dob edit`` and note the start and end time widget
    styles. Now shift focus to one of the widgets, and then away.

    - Depending on how the style is configured, the look of the widget
      after shifting focus away from it does not look like how it
      originally looked.

- Bugfix: Print error rather than crash on ``$EDITOR`` fail.

  - Use case: User sets their ``EDITOR`` environment variable to
    a bad path, or adds arguments (which is not supported -- but
    one could use an intermediate shell script wrapper to add args).

- Regression: Cannot enter colon (for clock time) in time widgets.

  - Solution: Only enable colon commands when content has focus.

- Feature: Set app background color via ``label = <>`` in styles.conf.

  - PTK already assigns 'class:label' to every widget. This updates the
    style-clobbering calls to maintain the label. Thus, user could add,
    say, ``label = 'bg:#00AA66'`` to their ``styles.conf``, to give the
    app a uniform background color.

- Improve: Make easier to base styles off 'night' and 'light' base styles.

  - Rather than assign the base color to all classes, which makes it
    difficult to override them in styles.conf (because user is then
    forced to override the highest-order class for every widget),
    leave all the class styles empty except for the lowest ordered
    class, which is common to all widgets, class:label.

- Improve: Use no precision in 'Gap Fact of' text until duration > 60 seconds.

  - Otherwise the footer status message updates too frequently,
    is too distracting.

- Improve: Require confirmation after printing errors on Carousel startup.

  - Instead of pausing after printing error messages, require user to
    confirm. Otherwise, user may not have time to read the errors. Also,
    after quitting Carousel, errors are still off-screen (up-screen).

- Improve: Warn when syntax errors found in style config.

1.1.1 (2020-04-20)
==================

- Regression: Fetching 'default' style fails during style config load.

1.1.0 (2020-04-20)
==================

- Bugfix: Import ``FactsDiff`` display broken.

- Bugfix: 'value-tags' class missing from hash-and-label tag parts' styles.

- Feature: New ``dob styles`` commands.

- Feature: New ``dob rules`` commands.

- Feature: New ``dob ignore`` commands.

- Feature: Make tags_tuples parts styleable (for ``git edit``).

- Feature: Make factoid parts styleable (for ``git show``).

- Tweak: Update 'night' style settings.

- Enhance: Apply 'value-tags' class to tags diff parts.

- API: Rename functions; move functions between libraries.

- API: Update renamed config setting: ``stylit_fpath`` → ``rules_fpath``.

1.0.10 (2020-04-17)
===================

- Improve: Remove requirement that custom paste config be numbered sequentially.

1.0.9 (2020-04-15)
==================

- Feature: Let user define custom key bindings for pasting arbitrary factoids.

  - I.e., user can map their own keys to setting Fact metadata,
    including the act\@gory, tags, and the description.

  - Usage: Add 2 settings to your user config for each custom mapping.

    - One setting specifies the Factoid to parse,
      and the other is the key binding to use.

    - Nest them under a new ``[custom-paste]`` section. Use the prefixes,
      ``factoid_`` and ``mapping_``, and start numbering from ``1``.

    - For instance, within ``~/.cache/dob/dob.conf``, here are
      some custom mappings::

          [custom-paste]

          # Paste act@gory and 2 tags:
          factoid_1 = "Tea@Personal: #biscuit #zinger"
          mapping_1 = f4

          # Paste act@gory, 1 tag, and a description (if not already set):
          factoid_2 = "Tickets@Project: #num-1234: Working on baloney."
          mapping_2 = f5

          # Paste a few tags (the @: is required):
          factoid_3 = "@: #tag-1 #tag-2"
          mapping_3 = f6

          # Paste a mere description:
          factoid_4 = "#this is not a tag"
          mapping_4 = f7

      Then, just press ``F4``, or ``F5``, etc., to apply to the current Fact.

      The user can choose whatever keybindings they want, and whatever metadata.

      Note that there's an arbitrary limit of 28 such custom paste commands.

  - See also ``dob add --help`` for a description of the Factoid format.

    Or just follow the formats in the example above.

- Feature: New command "shortcuts" (multiple command wrappers).

  - One command to copy the current Fact meta and paste to the final Fact.

    - Currently mapped to ``Ctrl-e``.

  - One command to copy the current Fact meta, stop the final Fact,
    and paste to the new active Fact.

    - Currently mapped to ``V``.

  - One command to stop the final Fact, switch to the new active Fact,
    and prompt for the act\@gory.

    - Currently mapped to ``o``.

- Bugfix: Entering date prefix but calling [count]-modified command crashes.

- Bugfix: Applying meaningless delta-time still marks Fact dirty nonetheless.

  - E.g., if Fact is 30 minutes wide, and you ``+30<TAB>`` to set end to
    30 minutes past start, Fact Diff would show no change, but on quit,
    dob would ask you to save.

- Bugfix: Rift jumpers change to first/final real Fact, not gap Fact.

- UX: Swap ``G``/``gg`` and ``f``/``F`` command mappings.

- Improve?: Update active gap Fact status on the tick.

  - Updates X.XX in the text, "Gap Fact of X.XX mins. [edit to add]."

  - Except change the precision to one, e.g., X.X mins, so it updates
    less frequently. Otherwise, if hundredths place showing, the status
    message and the Fact Diff end time (which shows <now>) update at
    slightly different rates, but similar enough that it looks weird.

1.0.8 (2020-04-14)
==================

- Bugfix: Crash handling clock time parse error.

  - Usually specifying clock time is okay, e.g., '100' is interpreted
    as 1:00a. But the hour and minute components were not being
    bounds-checked, i.e., 0..59. So, e.g., trying to decode '090'
    would crash (rather than be reported as not-a-date).

- Bugfix: Editor command handlers using stale "now".

  - So, e.g., if you started dob at 5p, and now it's 6p, and the current
    Fact is active (no end time), pressing 'J' to jump back a day would
    find Fact from yesterday at 5p, not 6p. (I'm sure there were more
    important use cases where this was more harmful, but this is the
    most obvious one to highlight.)

- Bugfix: Relative edit time feature broken/shadowed by delta-time bindings.

  - E.g., trying to type a relative time, say '+60', in the edit time widget
    was been intercepted by the newish delta-time feature. Consequently, the
    delta-time feature is now disabled when editing the start or end time.

- Bugfix: Commando save (``:w``) hides status message ('Saved {} Facts').

- Feature: Jump to date (using ``G`` or ``gg`` command modifier prefix).

  - E.g., ``20200410G`` will jump to first Fact on 2020-04-10.

  - User can specify (via config) allowable punctuation.

    - E.g., in addition to ``20200101G`` to jump to New Year's day, user
      can instead type ``2020-01-01G``, or ``2020/01/01G``, etc., depending
      on what ``date_separators`` are specified in the config.

  - More examples: ``100G`` jumps to Fact at 1:00 AM today.

    Or type ``2020/01/01 1400G`` or more simply ``2020010114G``
    to jump to 2p on New Year's day, 2020.

- Feature: Wire backspace to command modifier, commando, and time-delta modes.

  - Pressing backspace will (naturally) remove the last character typed
    from the command modifier/commando/time-delta being built, or it'll
    cancel the operation if nothing is left to remove.

- Feature: Add true first/final Fact jump commands.

  - Because ``G`` and ``gg`` stop on FactsManager group boundaries
    (these are the contiguous Fact "windows" the editor uses to
    store Facts in memory (which allows editing multiple Facts
    between database writes), and are used during the import process,
    which is really where stopping on group boundaries makes the most
    sense. In other words, we should probably make these commands the
    new ``G``/``gg``, and move the old commands to other key mappings.
    But I'm not ready to make that... leap).

  - The new commands are wired to ``f`` (final) and ``F`` (first) Fact jump.

- Improve: Show command modifier or delta-time in status as user types.

  - Might as well, because we already display the commando as it's built.
    And it provides context to the user, which could be a teachable moment,
    if the user is learning by mashing (keys).

- Improve: Support allow-gap toggling.

  - Now that the command modifier or time-delta is shown as a status
    message, it'll be obvious to the user if allow-gap is on or off.
    So pressing ``!!`` will first enable allow-gap, then disable it,
    rather than canceling the operation.

- Improve: Let user allow-gap (e.g., ``!``) before time-delta (``-``/``+``).

  - E.g., in addition to ``+10!<ENTER>``, ``!+10<ENTER>`` also now works.

- Improve: Wire Ctrl-C to clear or cancel command modifier/commando/delta-time.

- Improve: Allow Tab, in addition to Enter, to finish delta-time command.

  - Because Tab is the left hand's Enter.

- Improve: Make easy to set end to "now" on active Fact (e.g., via ``[`` or ``]``).

  - For active Fact, rather than the 1-minute decrement (``[``) and increment
    (``]``) operators using (now - 60 seconds) or (now + 60 seconds), just use
    now. (So if user wants to really remove 1 minute from now they can just
    press the key twice, e.g., ``[[``, or use a count modifier, e.g., ``1[``.)

- Improve: Linger to show 'Saved' message on save-and-exit commando (``:wq``).

- Improve: Pass carousel-active indicator to post processors.

  - So that plugins may behave differently when triggered by a save when dob
    is also quitting, versus a save from the interactive editor.

    - This is mostly useful so that a plugin does not errantly output any
      text to the display, which would mess up the editor interface.

- Improve: Add "from" to Jump Fact time reference status message, for context.

1.0.7 (2020-04-12)
==================

- Feature: Make all key bindings user configurable.

  - Run ``dob config dump editor-keys`` to see all the mappings.

  - User can specify zero, one, or multiple keys for each action.

- Improve: Remove 'escape'-only binding to avoid exit on unmapped Ctrl-keys.

- Bugfix: Catch Ctrl-C on dirty-quit confirmation, to avoid unseemly stack trace.

- Bugfix: Ctrl-W not saving on exit.

- Improve: Remove the Ctrl-W save-and-exit key binding.

  - Convention is that Ctrl-W is "close", but what would that be in dob?

  - The command remains but the binding was removed. The user can assign
    a key binding in their config if they want to enable this command.

- Feature: Vim-like command mode (lite).

  - Just the three commands, ``:w``, ``:q``, and ``:wq``.

  - Because dob uses EDITOR, if Vim is user's editor, user could
    run ``:wq`` twice in a row to save their Fact description, leave
    the Vim editor, and then save and quit dob.

- Feature: +/-N time adjustment commands.

  - Type minus to begin a start time adjustment command. E.g., if you
    want to set the start time to ten minutes before the end time, type
    ``-10<CR>``. Or type ``-10m`` (for minutes). For the active Fact, the
    time is calculated relative to "now".

  - Type a plus to begin an end time adjustment command, followed by
    an integer or floating point number, and then press Enter or "m"
    for minutes, or "h" for hours.

    - E.g., to set the end time 2.5 hours after the start time, type ``+2.5h``.

- Feature: Add modifier key (defaults to ``!``) to allow interval gap.

  - E.g., consider the  command ``-1h``, which sets start 1 hour before end.
    If it makes the current Fact's time shorter, then it stretches the
    previous Fact's end time, as well.

    - To not touch the neighbor Fact but to leave a gap instead,
      press the modifier key after entering the number, e.g., ``-1!h``.

  - User can change the modifier key via the ``editor-keys.allow_time_gap``
    config setting.

- Feature: Convenient 1- and 5-minute single-key time nudging commands.

  - E.g., ``[`` and ``]`` to decrement or increment end by 1 min., or
    add shift press for 5 mins., i.e., ``{`` and ``}``.

  - Likewise, use ``,`` and ``.`` to nudge start time
    backwards or forwards by 1 minute, respectively;
    and use ``<`` and ``>`` for five minutes instead.

  - All four keys are user-customizable, of course!

- Bugfix: Ensure Facts marked dirty after time nudging.

  - Or user is not asked to save on exit after nudging time.

- Bugfix: Long press time nudge is not increasing deltas over time.

  - E.g., if user holds Ctrl-left down, it starts adjusting the time by
    one minute for each press generated, but it was not increasing to
    five minutes per press, etc., the longer the user kept the key pressed.

- Improve: Ensure neighbor Fact time width not squashed to 0.

- Bugfix: Cannot jump to first/final fact if current Fact within jump delta.

  - E.g., Consider user is on current Fact, 2020-04-12 12:00 to 13:00, and
    the final Fact is from 2020-04-12 15:00 to 16:00. Pressing ``K`` does not
    jump to the final Fact, because it was less than 1 day ahead of current.

- Improve: On jump day from active Fact, use now as reference time.

  - This feels more natural, rather than jumping from the start of the
    active Fact, and prevents jumping back more than a day.

- Feature: Add Vim-like [count] prefix to Jump and Nudge commands.

  - E.g., user has been able to press ``j`` to go to the previous Fact.
    Now they can press ``5j`` to go back 5 Facts.

  - Likewise for jumping by day, e.g., ``2.5K`` will jump forward 2.5 days.

  - Same for time nudging, ``Ctrl-left`` has been used for decrementing the
    end time by 1 minute. Now user can specify exact amount, e.g., to
    decrease the end time by 4.2 minutes, the user can type ``4.2<Ctrl-left>``.

  - User can type ``!`` before or after digits to signal that a time nudge
    command should leave a gap rather than stretching a neighbor's time,
    e.g., ``!1<Ctrl-right>`` and ``1!<Ctrl-right>`` are equivalent.

  - To give user better visibility into what's happening, the jump commands
    now print a status message indicating how many days or number of Facts
    were jumped. When jumping by day, the time reference used is also shown,
    which is helpful if there's a long Fact or Gap, so the user does not get
    confused when their jump does not appear to do anything (i.e., when
    time reference changes but locates the same Fact that was showing).

1.0.6 (2020-04-10)
==================

- Enhance: Let user clear end time of final Fact.

1.0.5 (2020-04-09)
==================

- Bugfix: If you edit end to be before start, dob crashes after alert dialog.

- Improve: On neighbor time adjust, prefer fact_min_delta for min. time width.

1.0.4 (2020-04-08)
==================

- Bugfix: Changing focus breaks on Ctrl-S from time widget.

- Bugfix: Upstream PTK asynio upgrade breaks popup dialog.

  Aka, convert generator-based coroutines to async/await syntax.

- Bugfix: User unable to specify editor.lexer.

- Bugfix: Footer component class style (re)appended every tick.

1.0.3 (2020-04-01)
==================

- Bugfix: Send package name to get_version, lest nark use its own.

1.0.2 (2020-04-01)
==================

- Docs: Remove unnecessary version details from carousel help.

- Refactor: DRY: Use new library get_version.

1.0.1 (2020-03-31)
==================

- Bugfix: Repair demo command (fix class-name formation from tags containing spaces).

1.0.0 (2020-03-30)
==================

- Booyeah: Inaugural release (spin-off from |dob|_).

