# Issue Editor Templates

- *base.html* - A barebones extension of *bulletin/base.html*.

- *post.html* - Displays one Post; DOES NOT extend *base.html* (so no page headers or footers, for example, are displayed); includes *section.html* to display Post.sections.

- *post_list.html* - Displays a list of Posts, extends *post.html*.

- *section.html* - Displays one Section, like *post.html*, does NOT extend *base.html*; includes *section_post.html* to display Section.posts.

- *section_post.html* - Displays a list of Posts in a Section, does NOT extend *base.html*.

- *issue.html* - Displays one Issue, extends *base.html*.

- *issue_section_list.html* - Displays Sections in an Issue, extends *section.html*.

- *newsletter_issue_list.html* - Displays a list of Issues for a Newsletter, extends *issue.html*.

The goal was to provide "pluggable" templates, representing data components.  So there's a template to show a Post, one to show a Section, and one to show an Issue.  None of these extend base.html, so they have no page headers or footers, and this makes inclusion and extension of them easy.

There's a list view for each of Post, Section, and Issue, extending post.html, section.html, and issue.html, respectively. These are simple, views, essentially

    {% for object in object_list %}
      {{ block.super }}
    {% endfor %}

Two of the templates are included in others. *section.html* is included by *post.html* to display the Posts in a Section. This is a win, and actual reuse -- the same template, and so the same look and feel, is used to render the list of Sections in an Issue and the list of Sections associated with a Post. (As templates become more complex, this win throbs.)

Similarly, *section.html* includes *section_post.html* to display the Posts in a Section.

 Issue Editor Template Relationships
 +---------------------------------+

 +------------+ includes     +--------------+ includes  +--------------------+
 | post.html  +----------+-> | section.html +---------->| section_post.html  |
 +------------+          ^   +--------------+           +--------------------+
          ^              |           ^
          |              |           |
          | extends      |           | extends
 +--------+---------+    |  +---------+----------+
 | post_list.html   |    |  | issue_section.html |
 +------------------+    |  +--------------------+
                         |
                         |
        +-----------+    |
        | base.html |    +-----+
        +-----------+          |
             ^                 |
             | extends         |
       +-----+------+ includes |
       | issue.html +----------+
       +------------+
             ^
             | extends
 +-----------+----------------+
 | newsletter_issue_list.html |
 +----------------------------+
