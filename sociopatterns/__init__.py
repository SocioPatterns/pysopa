#!/usr/bin/env python
#
#  Copyright (C) 2008-2010 Istituto per l'Interscambio Scientifico I.S.I.
#  You can contact us by email (isi@isi.it) or write to:
#  ISI Foundation, Viale S. Severo 65, 10133 Torino, Italy. 
#
#  This program was written by Ciro Cattuto <ciro.cattuto@gmail.com>
#

# --------------------------------------------------------------------------

class Event(object):
    """
    Base class used for all events
    reported by the SocioPatterns/OpenBeacon infrastructure
    """
    __slots__ = ('t', 'ip', 'id', 'seq')

    def __init__(self, tstamp, ip, id, seq):
        self.t = tstamp
        self.ip = ip
        self.id = id
        self.seq = seq

    def get_hash(self):
        """
        The (tag id, sequence counter) combination uniquely identifies
        a packet in the air. This method returns an hash value
        computed from the above pair.
        """

        return hash( (self.id, self.seq) )


class Sighting(Event):
    """
    Class for Sighting objects.
    A sighting is a message emitted by one tag and received
    (possibly in multiple copies) by the infrastructure.
    A sighting only contains information about the tag that trasmitted it.
    """
    
    __slots__ = ('strength', 'flags', 'last_seen', 'boot_count')

    protocol = 24

    def __init__(self, tstamp, ip, id, seq, strength, flags, last_seen=0, boot_count=0):
        """
        Constructor of the Sighting class.
        Instances are typically built by an instance
        of the sociopatterns.Loader class,
        and made available as a stream using the iterator semantics.

        required parameters are:
        
        tstamp -- time of the event, as a UNIX ctime integer

        ip -- IP address of the reader that reported the event,
        represented as an unsigned 32-bit integer (10.254.0.1 is 0x0afe0001)

        id -- the unique ID of the tag emitting the packet (16-bit integer)

        seq -- sequence number of the packet, as a 32-bit integer.
        Packets with the same (id, seq) pair are duplicates reported
        by different readers (each packet having a different ip field).

        strenght -- power level at which the RF chip of the tag
        was asked to trasmit. Integer from 0 (lowest power)
        to 3 (highest power).

        flags -- one byte of flags.
        "Taps" on the RFID tags set bit 1.
        The "infected" flags of the Dublin experiment sets bit 2.

        keyword parameters are:

        last_seen -- the ID of the last tag that was seen
        by the trasmitting tag. Do no use this info for contact analysis.

        boot_count -- the number of reboot cycles the tag went through
        (16-bit integer). The counter is incremented every time the tag
        reboots. When the battery of a tag runs our, multiple and frequent
        reboots can be observed because of brown-outs.
        """

        Event.__init__(self, tstamp, ip, id, seq)

        self.strength = strength
        self.flags = flags
        self.last_seen = last_seen
        self.boot_count = boot_count

    def get_hash(self):
        return hash( (self.id, self.boot_count, self.seq) )

    def __repr__(self):
        """
        Returns a human-readable representation of the Sighting event,
        as an ASCII string.
        """

        return 'S %ld 0x%08x %d 0x%08x %d %d %s %s' % (self.t, self.ip, self.id, self.seq, self.strength, self.flags, self.last_seen, self.boot_count)


class Contact(Event):
    """
    Class for Contact objects.
    A contact is a message emitted by one tag and received
    (possibly in multiple copies) by the infrastructure.
    A contact contains information about the tag that trasmitted it
    as well as about tags lying in its proximity.
    """
    
    __slots__ = ('seen_id', 'seen_pwr', 'seen_cnt', 'flags', 'boot_count')

    protocol = 69

    def __init__(self, tstamp, ip, id, seq, seen_id=[], seen_pwr=[], seen_cnt=[], flags=0, boot_count=0):
        """
        Constructor of the Contact class.
        Instances are typically built by an instance
        of the sociopatterns.Loader class,
        and made available as a stream using the iterator semantics.

        required parameters are:
        
        tstamp -- time of the event, as a UNIX ctime integer

        ip -- IP address of the reader that reported the event,
        represented as an unsigned 32-bit integer (10.254.0.1 is 0x0afe0001)

        id -- the unique ID of the tag emitting the packet (16-bit integer)

        seq -- sequence number of the packet, as a 32-bit integer.
        Packets with the same (id, seq) pair are duplicates reported
        by different readers (each packet having a different ip field).

        keyword parameters are:

        seen_id -- list of 16-bit integers of the tags that were last seen
        by the reporting tag. The list contains unique tag IDs, at most
        4 of them. Its length is equal to the length of seen_pwr and seen_cnt.
        
        seen_pwr -- list of integers. Each element of the list represents
        the strength (0..3) of the weakest packet received from the tag
        in the corresponding position of the seen_id list.

        seen_cnt -- list of integers. Each element of the list represents
        the number of packets (1..7) received at the weakest power
        (seen_pwr) from the tag in the corresponding position of seen_id.

        flags -- one byte of flags

        boot_count -- the number of reboot cycles the tag went through
        (16-bit integer). The counter is incremented every time the tag
        reboots. When the battery of a tag runs our, multiple and frequent
        reboots can be observed because of brown-outs.
        """

        Event.__init__(self, tstamp, ip, id, seq)

        self.seen_id = seen_id
        self.seen_pwr = seen_pwr
        self.seen_cnt = seen_cnt
        self.flags = flags
        self.boot_count = boot_count
        

    def __repr__(self):
        """
        Returns a human-readable representation of the Contact event,
        as an ASCII string.
        """

        clist = ""
        for (id2, pwr, count) in zip(self.seen_id, self.seen_pwr, self.seen_cnt):
            clist += " [%d(%d) #%d]" % (id2, pwr, count)

        return 'C %ld 0x%08x %d 0x%04x 0x%08x %d%s' % (self.t, self.ip, self.id, self.boot_count, self.seq, self.flags, clist)


