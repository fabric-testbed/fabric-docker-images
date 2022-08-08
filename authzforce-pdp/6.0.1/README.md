# Special provisions for version 6.0.1


## Migration from earlier versions

Version 6.0.1 (Version 20 of CLI) requires using an updated namespace in `pdp.xml`.
- Summary of changes https://github.com/authzforce/core/blob/develop/CHANGELOG.md#1800
- Migration procedure details https://github.com/authzforce/core/blob/develop/MIGRATION.md#migration-from-version-17x-to-18x-and-later

Really just the namespace version needs to be updated:
- Replace the namespace "http://authzforce.github.io/core/xmlns/pdp/7" with "http://authzforce.github.io/core/xmlns/pdp/8"
- Change version "7.1 to "8.0".

This docker definition already contains the updated `pdp.xml` so it will work 'from scratch', it will also proactively
attempt to update existing `pdp.xml` to the new version. However for completeness here is how it is done
(depending on whether you are on a Mac or Linux system you may or may not need space between `.tmp` and the `-i` option):
```
$ sed -e 's_pdp/7_pdp/8_' -e 's_7.1_8.0_' -i .tmp pdp.xml
$ rm pdp.xml.tmp
```
