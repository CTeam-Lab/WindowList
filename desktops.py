import subprocess
import collections
import socket
import os
import yaml

class Create():
    def __init__(self):

        CURRENT_DIR = os.path.dirname(__file__)
        config_path = os.path.join(CURRENT_DIR, 'blacklist.yml')
        self.config = yaml.load(file(config_path))


    def get_desktops(self):
        desktop_list = {}
        windows_list = self.get_windows();

        p1 = subprocess.Popen(['wmctrl','-d'], stdout=subprocess.PIPE)
        (sout,serr) = p1.communicate()

        for line in sout.split('\n'):
            if not line:
                continue

            id = line.split(' ')[0]
            title = line.split(' ')[-1]

            # add desktops
            desktop_list[id] = {'title': title, 'windows': {}}

            # add windows to the desktops
            for window in windows_list:
                if window['desktop_id'] == int(id):
                    desktop_list[id]['windows'][window['id']] = window['title']

        for desktop in desktop_list.keys():
            if len(desktop_list[desktop]['windows']) == 0:
                del desktop_list[desktop]

        # Sort the list
        return collections.OrderedDict(sorted(desktop_list.items()))

    def get_windows(self):
        new_window_list = []

        p1 = subprocess.Popen(['wmctrl','-l'], stdout=subprocess.PIPE)
        (sout,serr) = p1.communicate()

        hostname = socket.gethostname()

        # ugly get list, XLIB/XCB coming soon
        for line in sout.split('\n'):
            if hostname in line:

                id = line.split(' ')[0]

                desktop_id = line.split(' ')[2] or 0

                '''
                Sometimes it can bring trash, we just want digits
                '''
                if desktop_id.isdigit() == False:
                    continue

                # grab title, preserving whitespace
                title_pos = len(id) + len(hostname) + 5
                title = line[title_pos:]

                flag = 0
                for s in self.config['blacklist']:
                    if title in s:
                        flag = 1
                        break

                # ugly parent continue
                if flag == 1:
                    flag = 0
                    continue

                window = {
                    'id': id,
                    'title': title,
                    'desktop_id': int(desktop_id)
                }

                new_window_list.append(window)

        return new_window_list