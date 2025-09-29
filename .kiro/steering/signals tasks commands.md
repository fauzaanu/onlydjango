# Signals, tasks, commands and the messages framework

Signals are important, use them when it makes sense to use them. For heavy operations create a signal that calls a huey task so it wont block.

Within the view we should include calls to django messages framework so that users can get one time notifications and our templates should obviousely support the UI of them.

Most tasks that are triggered should be triggerable with a management command, this will also make it easier to isolate certain functions and manually test somethings that are very hard to test on a usual code based test.

> TLDR: Use signals, tasks, management commands and django messages framework in a wholesome way