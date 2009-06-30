#!/usr/bin/env python

"""Unittest for kegbot module"""

import commands
import time
import logging
import socket
import unittest
import kegbot

from django.test import TestCase

from pykeg.core import defaults
from pykeg.core import event
from pykeg.core import models
from pykeg.core import kb_common
from pykeg.core.net import kegnet
from pykeg.scripts import gentestdata

LOGGER = logging.getLogger('unittest')

class KegbotTestCase(TestCase):
  def setUp(self):
    del logging.root.handlers[:]
    defaults.set_defaults()
    gentestdata.set_data()

    self.kegbot = kegbot.KegbotCoreApp(daemon=False)
    self.env = self.kegbot._env

    # Kill the kegbot flow processing thread so we can single step it.
    self.service_thread = self.env._service_thread
    self.env._threads.remove(self.service_thread)

    self.kegbot._Setup()
    self.kegbot._StartThreads()

  def tearDown(self):
    for thr in self.env.GetThreads():
      self.assert_(thr.isAlive(), "thread %s died unexpectedly" % thr.getName())
    self.kegbot.Quit()
    for thr in self.env.GetThreads():
      self.assert_(not thr.isAlive(), "thread %s stuck" % thr.getName())
    del self.kegbot
    del self.env

  def testSimpleFlow(self):
    addr = (kb_common.KEGNET_SERVER_BIND_ADDR,
            kb_common.KEGNET_SERVER_BIND_PORT)
    client = kegnet.KegnetClient(addr, 'testclient')
    client.Login()

    # Synthesize a 2100-tick flow. The FlowManager should zero on the initial
    # reading of 1000.
    client.StartFlow('meter0')
    client.FlowUpdate('meter0', 1000)
    client.FlowUpdate('meter0', 1100)
    client.FlowUpdate('meter0', 2100)
    client.FlowUpdate('meter0', 3100)
    client.FlowUpdate('meter0', 3200)
    client.StopFlow('meter0')

    self.service_thread._FlushEvents()

    # Services the flow thread (flush all events)

    drinks = models.Drink.objects.all().order_by('-id')
    last_drink = drinks[0]

    LOGGER.info('last drink: %s' % (last_drink,))
    self.assertEquals(last_drink.ticks, 2200)

if __name__ == '__main__':
  unittest.main()
