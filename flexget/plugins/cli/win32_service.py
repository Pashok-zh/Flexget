import argparse
import sys

import flexget
from flexget import options
from flexget.event import event

def do_cli(manager, options):
    import pythoncom
    import win32serviceutil
    import win32service
    import win32event
    import servicemanager
    import socket

    class AppServerSvc (win32serviceutil.ServiceFramework):
        _svc_name_ = "FlexGet"
        _svc_display_name_ = "FlexGet Daemon"

        def __init__(self, args):
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            socket.setdefaulttimeout(60)

        def SvcStop(self):
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.hWaitStop)

        def SvcDoRun(self):
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                  servicemanager.PYS_SERVICE_STARTED,
                                  (self._svc_name_, ''))
            self.main()

        def main(self):
            flexget.main(['daemon'])

    argv = options.args
    if options.help:
        argv = []

    # Hack sys.argv a bit so that we get a better usage message
    sys.argv[0] = 'flexget service'
    win32serviceutil.HandleCommandLine(AppServerSvc, argv=['flexget service'] + options.args)


@event('options.register')
def register_parser_arguments():
    parser = options.register_command('service', do_cli, help='view and manipulate the series plugin database',
                                      add_help=False)
    parser.add_argument('--help', '-h', action='store_true')
    parser.add_argument('args', nargs=argparse.REMAINDER)