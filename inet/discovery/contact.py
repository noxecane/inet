from collections import namedtuple
from inet import messaging as msg
from pyfunk import combinators as cm

Contact = namedtuple('Contact', ['address', 'services'])


class MethodNotFound(AttributeError):
    pass


@msg.invalid_type
def to_contact(msg):
    '''
    Converts a dict to a contact tuple
    @sig to_contact :: Dict -> Contact
    '''
    return Contact(**msg)


@cm.curry
def get_contact(contacts, path):
    '''
    Tries to retrive a contact based on the given service path and raises
    MethodNotFound exception if the path has no contact.
    @sig get_contact :: Dict Str -> Str -> Str
    '''
    try:
        return contacts[path]
    except KeyError:
        raise MethodNotFound('The given path "%s" was not found' % path)


@cm.curry
def add_contact(contacts, contact):
    '''
    Adds a contact's service paths to the contacts datastructure and
    points them to their address.
    @sig add_contact :: Dict Str -> Contact -> Dict Str
    '''
    for s in contact.services:
        contacts[s] = contact.address
    return True


def contacts():
    '''
    Creates a contact mapping and return setter, getter tuple.
    The setter uses a contact object to update the map while
    the getter returns the address a service is mapped to.
    @sig contacts :: _ -> ((Contact -> Bool), (Str -> Str))
    '''
    contacts_map = {}
    return add_contact(contacts_map), get_contact(contacts_map)
