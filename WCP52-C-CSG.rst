:Title: C Coding Style Guidelines
:Author:
    Chris Pavlina <cpavlin1@binghamton.edu>;
    adapted from Python PEP-8, placed in the public domain.
:Content-Type: text/x-rst
:Created: 2014-10-24

Introduction
============

This document provides coding conventions for WCP52, Gain/Phase Analyzer,
for use with code written in C and similarly structured languages (e.g.
C++, Java).

This document has been heavily adapted from the Python Software Foundation's
"PEP-8: Style Guide for Python Code", which they have placed into the public
domain.


Code lay-out
============

Indentation
-----------

Use 4 spaces per indentation level.

Continuation lines should align wrapped elements etiher vertically
or using a hanging indent. When using a hanging indent the following
considerations should be applied: there should be no arguments on the
first line and further indentations should be used to clearly
distinguish itself as a continuation line.

Yes::

    // Aligned with opening delimiter.
    foo = long_function_name(var_one, var_two,
                             var_three, var_four);

    // More indentation included to distinguish this from the rest.
    int long_function_name(
            int var_one, int var_two, int var_three,
            int var_four)
    {
        printf ("%d\n", var_one);
    }

    // Hanging indents should add a level.
    foo = long_function_name(
        var_one, var_two,
        var_three, var_four);

No::

    // Arguments on first line forbidden when not using vertical alignment.
    foo = long_function_name(var_one, var_two,
        var_three, var_four);

    // Further indentation required as indentation is not distinguishable.
    int long_function_name(
        int var_one, int var_two, int var_three,
        int var_four)
    {
        printf ("%d\n", var_one);
    }

The 4-space rule is optional for continuation lines.

Optional::

    // Hanging indents *may* be indented to other than 4 spaces.
    foo = long_function_name(
      var_one, var_two,
      var_three, var_four)

.. _`multiline if-statements`:

When the conditional part of an ``if``-statement is long enough to require
that it be written across multiple lines, it's worth noting that the
combination of a two-character keyword (e.g. ``if``), plus a single space,
plus an opening parenthesis creates a natural 4-space indent for the
subsequent lines of the multiline conditional.  This can produce a visual
conflict with the indented suite of code nested inside the ``if``-statement,
which would also naturally be indented to 4 spaces.  We take no
explicit position on how (or whether) to further visually distinguish such
conditional lines from the nested suite inside the ``if``-statement.
Acceptable options in this situation include, but are not limited to::

    // No extra indentation.
    if (this_is_one_thing &&
        that_is_another_thing) {
        do_something ();
    }

    // Prefer to place the opening brace on a separate line.
    if (this_is_one_thing &&
        that_is_another_thing)
    {
        do_something ();
    }

    // Add some extra indentation on the conditional continuation line.
    if (this_is_one_thing &&
            that_is_another_thing) {
        do_something ();
    }

The closing brace/bracket/parenthesis on multi-line constructs may
either line up under the first non-whitespace character of the last
line of list, as in::

    int my_list[] = {
        1, 2, 3,
        4, 5, 6,
        };
    result = some_function_that_takes_arguments(
        'a', 'b', 'c',
        'd', 'e', 'f',
        );

or it may be lined up under the first character of the line that
starts the multi-line construct, as in::

    int my_list[] = {
        1, 2, 3,
        4, 5, 6,
    };
    result = some_function_that_takes_arguments(
        'a', 'b', 'c',
        'd', 'e', 'f',
    );


Tabs or Spaces?
---------------

Spaces are the preferred indentation method.

Tabs should be used solely to remain consistent with code that is
already indented with tabs.

Mixing tabs and spaces is disallowed.


Maximum Line Length
-------------------

We do not impose a maximum line length, but lines which are longer than
79 character should be taken note of, as this may be a sign that they
would be more understandable if restructured.


Blank Lines
-----------

Separate top-level function definitions with two blank lines.

Extra blank lines may be used (sparingly) to separate groups of
related functions. Blank lines may be omitted between a bunch of
related one-line functions (e.g. a set of dummy implementations).

Use blank lines in functions, sparingly, to indicate logical sections.


Includes
--------

Includes are always put at the top of the file, just after any file
comments, and before declared globals and constants.

Includes should be grouped in the following order:

1. standard library headers
2. third-party headers
3. local application/library-specific headers

You should put a blank line between each group of includes.


Whitespace in Expressions and Statements
========================================

Pet Peeves
----------

Avoid extraneous whitespace in the following situations:

- Immediately inside parentheses, brackets or braces. ::

      Yes: spam(ham[1], (struct eggs_t) {eggs, 2})
      No:  spam( ham[ 1 ], (struct eggs_t) { eggs, 2 } )

- Immediately before a comma, semicolon, or colon::

      Yes: printf ("%d: %f\n", 1, 3.14159);
      No:  printf ("%d: %f\n" , 1 , 3.14159)  ;

- Immediately before the open parenthesis that starts the argument
  list of a function call::

      Yes: spam(1)
      No:  spam (1)

- Immediately before the open bracket that starts an indexing::

      Yes: dct[key] = lst[index]
      No:  dct [key] = lst [index]

- More than one space around an assignment (or other) operator to
  align it with another.

  Yes::

      x = 1;
      y = 2;
      long_variable = 3;

  No::

      x             = 1;
      y             = 2;
      long_variable = 3;


Other Recommendations
---------------------

- Always surround these binary operators with a single space on either
  side: assignment (``=``), augmented assignment (``+=``, ``-=``
  etc.), comparisons (``==``, ``<``, ``>``, ``!=``, ``<>``, ``<=``,
  ``>=``), Booleans (``&&``, ``||``, ``!``).

- If operators with different priorities are used, consider adding
  whitespace around the operators with the lowest priority(ies). Use
  your own judgment; however, never use more than one space, and
  always have the same amount of whitespace on both sides of a binary
  operator.

  Yes::

      i = i + 1;
      submitted += 1;
      x = x*2 - 1;
      hypot2 = x*x + y*y;
      c = (a+b) * (a-b);

  No::

      i=i+1;
      submitted +=1;
      x = x * 2 - 1;
      hypot2 = x * x + y * y;
      c = (a + b) * (a - b);

- Compound statements (multiple statements on the same line) are
  generally discouraged.

  Yes::

      if (foo == blah) {
          do_blah_thing();
      }
      do_one();
      do_two();
      do_three();

  Rather not::

      if (foo == blah) do_blah_thing();
      do_one(); do_two(); do_three();

- While sometimes it's okay to put an if/for/while with a small body
  on the same line, never do this for multi-clause statements.  Also
  avoid folding such long lines!

  Rather not::

      if (foo == blah) do_blah_thing();
      while (t < 10) t = delay();

  Definitely not::

      if (foo == blah) do_blah_thing();
      else do_non_blah_thing();

      do_one(); do_two(); do_three(long, argument,
                                   list, like, this);

      if (foo == 'blah') one(); two(); three();


Comments
========

Comments that contradict the code are worse than no comments.  Always
make a priority of keeping the comments up-to-date when the code
changes!

Comments should be complete sentences.  If a comment is a phrase or
sentence, its first word should be capitalized, unless it is an
identifier that begins with a lower case letter (never alter the case
of identifiers!).

If a comment is short, the period at the end can be omitted.  Block
comments generally consist of one or more paragraphs built out of
complete sentences, and each sentence should end in a period.

You should use two spaces after a sentence-ending period.

When writing English, follow Strunk and White.

Block Comments
--------------

Block comments generally apply to some (or all) code that follows
them, and are indented to the same level as that code. Block comments
follow the usual format::

    /* This is a block comment.
     * This is more block comment.
     */

Boxed comments may be used to draw particular attention (for example,
separating sections of a file)::

    /***************************************
     * I really, really like this comment. *
     ***************************************/

Inline Comments
---------------

Use inline comments sparingly.

An inline comment is a comment on the same line as a statement.
Inline comments should be separated by at least two spaces from the
statement.  They should start with a // and a single space.

Inline comments are unnecessary and in fact distracting if they state
the obvious.  Don't do this::

    x = x + 1                 // Increment x

But sometimes, this is useful::

    x = x + 1                 // Compensate for border

Documentation Comments
----------------------

Documentation comments should be written in block format and should list
all inputs, outputs, preconditions, postconditions, and side-effects when
applicable. The descriptions should begin with a single sentence, terminated
with a period (.), which summarizes the function as well as possible.  Use the
double-asterisk style to differentiate this, as documentation generation
software can recognize them::

    /**
     * Do something. This function takes things, puts out things, and
     * does things with other things.
     *
     * \param spam  A thing
     * \param eggs  Another thing
     * \return      More things

     * \pre     The things must be things.
     * \post    The things will still be things.
     * \sideeffect  Formats entire hard disk
     */

When possible, use Doxygen-compatible tags, as shown in the above example.


Naming Conventions
==================

Overriding Principle
--------------------

Names that are visible to the user as public parts of the API should
follow conventions that reflect usage rather than implementation.

Descriptive: Naming Styles
--------------------------

There are a lot of different naming styles.  It helps to be able to
recognize what naming style is being used, independently from what
they are used for.

The following naming styles are commonly distinguished:

- ``b`` (single lowercase letter)
- ``B`` (single uppercase letter)
- ``lowercase``
- ``lower_case_with_underscores``
- ``UPPERCASE``
- ``UPPER_CASE_WITH_UNDERSCORES``
- ``CapitalizedWords`` (or CapWords, or CamelCase -- so named because
  of the bumpy look of its letters).  This is also sometimes known
  as StudlyCaps.

  Note: When using abbreviations in CapWords, capitalize all the
  letters of the abbreviation.  Thus HTTPServerError is better than
  HttpServerError.
- ``mixedCase`` (differs from CapitalizedWords by initial lowercase
  character!)
- ``Capitalized_Words_With_Underscores`` (ugly!)

There's also the style of using a short unique prefix to group related
names together.  This is not used much in Python, but it is mentioned
for completeness.  For example, the ``stat(2)`` function fills a
structure whose items traditionally have names like ``st_mode``,
``st_size``, ``st_mtime`` and so on. This is useful in languages without
namespaces, such as C.

In addition, the following special forms using leading or trailing
underscores are recognized (these can generally be combined with any
case convention):

- ``_single_leading_underscore``: weak "internal use" indicator.
  Typically implies that the object with this name is declared ``static``.

- ``single_trailing_underscore_``: used by convention to avoid
  conflicts with keyword, e.g. ::

      toplevel(master, struct_=1);

Prescriptive: Naming Conventions
--------------------------------

Names to Avoid
~~~~~~~~~~~~~~

Never use the characters 'l' (lowercase letter el), 'O' (uppercase
letter oh), or 'I' (uppercase letter eye) as single character variable
names.

In some fonts, these characters are indistinguishable from the
numerals one and zero.  When tempted to use 'l', use 'L' instead.

File Names
~~~~~~~~~~

Files should have short, all-lowercase names.  Underscores can be
used in the file name if it improves readability.

Since some file systems are case insensitive and truncate long names, it is
important that file names be chosen to be fairly short and unique regardless of
case -- this won't be a problem on Unix, but it may be a problem when the code
is transported to older Mac or Windows versions, or DOS.

Global Variable Names
~~~~~~~~~~~~~~~~~~~~~

Global variables should be named in uppercase with a prefix of ``G_``::

    G_GLOBAL

Function Names
~~~~~~~~~~~~~~

Function names should be lowercase, with words separated by
underscores as necessary to improve readability.

Function and method arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a function argument's name clashes with a reserved keyword, it is
generally better to append a single trailing underscore rather than
use an abbreviation or spelling corruption.  Thus ``struct_`` is better
than ``strct``.  (Perhaps better is to avoid such clashes by using a
synonym.)

Constants
~~~~~~~~~

Constants are usually defined on a compilation unit level and written in all
capital letters with underscores separating words.  Examples include
``MAX_OVERFLOW`` and ``TOTAL``. Prefer ``const`` constants to preprocessor
macros.

