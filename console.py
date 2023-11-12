#!/usr/bin/python3
"""Command interpreter Entry point."""

import cmd
import re
import json
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):

    """Cmd class."""

    prompt = "(hbnb) "

    def _EOFhandle(self, line):
        """Handles EOF to exit.
        """
        print()
        return True

    def _quithandle(self, line):
        """Exits by Quit command.
        """
        return True

    def _emptyline(self):
        """Do nothing when ENTER.
        """
        pass

    def default(self, line):
        """Handle commands when no matches found"""
        self._checksyntax(line)

    def _checksyntax(self, line):
        """Test commands for syntax()"""
        ismatch = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not ismatch:
            return line
        reprclass = ismatch.group(1)
        mymethod = ismatch.group(2)
        args = ismatch.group(3)
        _uid_args_match = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if _uid_args_match:
            userid = _uid_args_match.group(1)
            _dict_attr = _uid_args_match.group(2)
        else:
            userid = args
            _dict_attr = False

        attr_and_value = ""
        if mymethod == "update" and _dict_attr:
            match_dict = re.search('^({.*})$', _dict_attr)
            if match_dict:
                self._dictupdate(reprclass, userid, match_dict.group(1))
                return ""
            _attr_value_match = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', _dict_attr)
            if _attr_value_match:
                attr_and_value = (_attr_value_match.group(
                    1) or "") + " " + (_attr_value_match.group(2) or "")
        cmnd = mymethod + " " + reprclass + " " + userid + " " + attr_and_value
        self.onecmd(cmnd)
        return cmnd

    def _create(self, line):
        """Creates a new instance.
        """
        if line == "" or line is None:
            print("** class name missing **")
        elif line not in storage.myclasses():
            print("** class doesn't exist **")
        else:
            ins = storage.myclasses()[line]()
            ins.save()
            print(ins.id)

    def _show(self, line):
        """Shows the instance string repr.
        """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            substrings = line.split(' ')
            if substrings[0] not in storage.myclasses():
                print("** class doesn't exist **")
            elif len(substrings) < 2:
                print("** instance id missing **")
            else:
                qk = "{}.{}".format(substrings[0], substrings[1])
                if qk not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[qk])

    def _destroyhandle(self, line):
        """Destroy an instance based on the name & id of class.
        """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            substrings = line.split(' ')
            if substrings[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(substrings) < 2:
                print("** instance id missing **")
            else:
                qk = "{}.{}".format(substrings[0], substrings[1])
                if qk not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[qk]
                    storage.save()

    def _allhandle(self, line):
        """Shows all instances of string repr.
        """
        if line != "":
            substrings = line.split(' ')
            if substrings[0] not in storage.myclasses():
                print("** class doesn't exist **")
            else:
                newl = [str(obj) for qk, obj in storage.all().items()
                      if type(obj).__name__ == substrings[0]]
                print(newl)
        else:
            _listnew = [str(obj) for qk, obj in storage.all().items()]
            print(_listnew)

    def _counthandle(self, line):
        """Returns the numbers of class instances.
        """
        substrings = line.split(' ')
        if not substrings[0]:
            print("** class name missing **")
        elif substrings[0] not in storage.myclasses():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    substrings[0] + '.')]
            print(len(matches))

    def _dictupdate(self, reprclass, userid, _dict):
        """Supportive method to update() the dictionary."""
        str = _dict.replace("'", '"')
        doc = json.loads(str)
        
        if not reprclass:
            print("** class name missing **")
        elif reprclass not in storage.myclasses():
            print("** class doesn't exist **")
        elif userid is None:
            print("** instance id missing **")
        else:
            qk = "{}.{}".format(reprclass, userid)
            if qk not in storage.all():
                print("** no instance found **")
            else:
                attrs = storage.myattributes()[reprclass]
                for attribute, val in doc.items():
                    if attribute in attrs:
                        val = attrs[attribute](val)
                    setattr(storage.all()[qk], attribute, val)
                storage.all()[qk].save()

    def _updatehandle(self, line):
        """Updates by changing attribute.
        """
        if line == "" or line is None:
            print("** class name missing **")
            return

        sent = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        ismatch = re.search(sent, line)
        reprclass = ismatch.group(1)
        userid = ismatch.group(2)
        attribute = ismatch.group(3)
        val = ismatch.group(4)
        if not ismatch:
            print("** class name missing **")
        elif userid is None:
            print("** instance id missing **")
        elif reprclass not in storage.myclasses():
            print("** class doesn't exist **")
        else:
            qk = "{}.{}".format(reprclass, userid)
            if qk not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not val:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', val):
                    if '.' in val:
                        cast = float
                    else:
                        cast = int
                else:
                    val = val.replace('"', '')
                attrs = storage.myattributes()[reprclass]
                if attribute in attrs:
                    val = attrs[attribute](val)
                elif cast:
                    try:
                        val = cast(val)
                    except ValueError:
                        pass
                setattr(storage.all()[qk], attribute, val)
                storage.all()[qk].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()

