from __future__ import print_function
# Copyright 2014 Kegbot Project contributors
#
# This file is part of the Pykeg package of the Kegbot project.
# For more information on Pykeg or Kegbot, see http://kegbot.org/
#
# Pykeg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Pykeg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pykeg.  If not, see <http://www.gnu.org/licenses/>.

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from pykeg.core import models


class Command(BaseCommand):
    args = '<description>'
    help = 'Creates an API key with the given description.'

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('Must specify description')

        key = models.ApiKey.objects.create(description=args[0])
        print(key.key)
