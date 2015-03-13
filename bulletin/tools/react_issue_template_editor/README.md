Dofta is a React-based Issue Template editor.

If/when it proves itself suitable for production, it will receive a
suitable new name.  Like "Issue Template Editor" or something else
boring like that.  Nothing with the pizazz of 'dofta'!

You must run `npm install` from this subdirectory, before running the
development server.

For the development server to find project static files, two steps
must be taken:

1.  run `./manage.py collectstatic`.

2.  ln the subdirectory created by collectstatic into the `src`
    directory. e.g.;

    $ ROOT=/Users/human/dev/bulletin
    $ ln -s $ROOT/static $ROOT/apps/dofta/src/

Run the development server with `grunt serve`.

There's a hard-coded URL in DoftaApp.jsx that points to a server
exposing the bulletin API.
