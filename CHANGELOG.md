# Changelog

Every noteable change is logged here.

## v0.25.3 (2022-12-18)

### Chore

* upgrade Jenkinsfile (7039af6ffeef)

## v0.25.2 (2022-12-18)

### Chore

* add rebase step (834c20a3d58a)
* upgrade requirements.txt (dbe1a9f64a35)
* upgrade pipe library (ca89f1eff71a)

## v0.25.1 (2022-12-14)

### Chore

* upgrade Pipeline (c93ecb793b59)
* upgrade requirements.txt (f8efc7908c20)

## v0.25.0 (2022-11-02)

### Feature

* use utila to have central cache control (d8ddffd8b37c)

## v0.24.0 (2022-10-27)

### Feature

* add data type kb, mb, gb (6543a443f71a)
* add api and secret key (d47a73c49aea)

## v0.23.0 (2022-10-27)

### Feature

* log variable skip (dc16e6eef5f2)
* add second, minute and hour (f6ba3132e1d7)
* enable holy value error (52d8dd1b3010)
* determine names before check to ease debugging (581ca3acbce8)
* clarify error message (bba311e82029)

### Fix

* adjust error message (2173069d1453)

### Chore

* convert nightly to all (be43d40f0a2e)
* upgrade environment (6e16b2ba6e27)
* upgrade requirements.txt (9f82f4c10909)

## v0.22.0 (2022-10-07)

### Feature

* add method to create tmp dirs (bf8603505193)

## v0.21.2 (2022-10-05)

### Chore

* upgrade requirements.txt (fdfc4da483e0)
* increase baw version (79a8284de027)
* root user is not necessary (fbd13adc7f54)

## v0.21.1 (2022-09-28)

### Fix

* add default docs path (70d557226171)

### Chore

* add git to generate project (2c51f8214a56)
* add Jenkinsfile (a62c555bbe3a)
* upgrade requirements.txt (40265ba3b871)

## v0.21.0

### Feature

* add minus type (56ddbd364c80)

## v0.20.0

### Feature

* add option to change test command (25bb4f6f244a)
* log optimization output path (e2874976709f)
* add parameter to change reduction steps (7c84a04a1188)
* add method to remove from global path (261de660b436)
* add method to extend path var (1653d8446b58)
* add brackets lookup (69ed0327f4c7)

### Fix

* disable cprofile (8513212b2108)

### Documentation

* adjust lookup information (5d821b153a0f)

## v0.19.1

### Feature

* adjust cache size (74d6c9e27a8f)

## v0.19.0

### Feature

* add methods to shorten caches (bee28be36430)
* round percent to ease debugging (d046cf1c83f7)

## v0.18.0

### Feature

* add HolyRate to create count dependent rate (841e836d79b4)

### Documentation

* adjust modules path (f633a80430b7)
* Happy New Year! (9f96b13a4529)

## v0.17.0

### Feature

* cache environment variable (0e2ac01623db)
* make env vars group able (3b0ffa6e48f7)

## v0.16.3

### Feature

* make holy value hash able (a17b6ece0787)

## v0.16.2

### Feature

* add bool comparison (c9ca7339df4a)
* add hv bool (80fa4f11eebf)

### Fix

* enable using holy values as tuple (c9d7ac681f9e)

## v0.16.1

### Fix

* add str lookup (824d8a2e2b9f)

## v0.16.0

### Feature

* support slicing for holy values (ae140b4834b8)
* add more debugging information (85c76f96d01c)

## v0.15.1

### Feature

* add caching mechanism to improve lookup time (cce7fd286e5a)

## v0.15.0

### Feature

* introduce algorithm to change a single value (214b591f5483)
* add option to display result (62f0215a4d84)
* add option to run test before optimization (39bd28acc4c2)

### Fix

* enable hard error later (38a982ac8881)
* add csv header and use comma (321c733c0794)
* use random selection when generated count (90f527337f23)

## v0.14.0

### Feature

* debug loading holy value file (f277cb84d0bc)
* improve plan creator (b80d18d5adb0)
* add option to load config from file (ae20b56a607a)
* create plan from config (b233b5e4989c)
* add optimization step (a2998dbcfb90)

### Fix

* ensure to have valid variable names (d6286f895c2c)
* use None if HC is not defined (bef450dd14e8)

## v0.13.0

### Feature

* use cloud base as default cloud path (5135497bd5ac)
* introduce cloud_base to setup cloud base path (bcacee371c7f)
* add option to return None as default value (bdc13faf81f5)
* add option to set and unset cloud links (81aa431e34b6)
* add cloud to load holy value table from env variables (be88b4a837e4)
* add base option to load config from different path (c3732baa14c7)
* strip newlines before and after collection (1c137717ca9a)
* extend basic arithmetic support (89c542ab16b0)
* add failure when no HolyValue is detected (d60c4c7b75f1)

### Fix

* verify data and limit at definition time (d8e5633c3365)
* collect table default correctly (58d13cba2033)
* validate float correctly (55097c0b8b2c)

## v0.12.0

### Feature

* add parameter to skip skipping files (ed7c30e1ebb3)
* skip build and tests folder (01076461595b)
* print banner after every collection step (86da6afbddce)
* add cli to generate holy value configuration (4e1981b57ac7)
* do not fail on importing error (af5f10063117)
* add support HolyTable to config generator (1f5d6f3452e5)
* use common mixin (1373497d15f3)
* harden collector (f0dbd5c84312)

## v0.11.0

### Feature

* add holy string (29e30c10d3f8)
* change default behavior (9cd2470fc87c)

## v0.10.1

### Feature

* clarify error message (743b18b13574)

### Fix

* adjust error message (d0e3f1a81541)

## v0.10.0

### Feature

* add HolyList (6a39490705e8)
* add default key option (91ce8bd9f9d7)

## v0.9.0

### Feature

* add option to manager debug state (01891100eedf)
* introduce holyvalue base exception (204b823ecabb)
* add methods to manage environment variables (d199d043a5cc)

### Documentation

* Happy New Year! (828e0dd1e3df)

## v0.8.7

### Fix

* catch invalid group determination (ac0358b4a04d)

## v0.8.6

## v0.8.3

### Documentation

* extend interface documentation (9b5f5869d570)

## v0.8.0

### Feature

* add holy table object (3e105571920e)

## v0.7.3

## v0.7.0

### Feature

* add holyvalue `BOOL` to public API (451e0af101d5)

## v0.6.18

## v0.6.0

### Feature

* add link to generated docs (b4ac084e1c5e)

## v0.5.17

## v0.5.0

### Feature

* add dunder methods to ease using of HolyValues (703ffe3b068a)
* ensure that holyvalue interface is used in a correct way (51c93626a57e)

### Documentation

* extend interface documentation (9aee69d38824)
* add general doc structure (1124d95e29ea)
* extend interface documentation (51050a59f084)

## v0.4.4

## v0.4.1

### Documentation

* Happy New Year! (40a3d4134ee9)

## v0.4.0

### Feature

* ensure to detect correct group and hv name (614e4b90c913)
* extend information of invalid holyvalue exception (7cb33c49de9e)
* validate holy value at runtime (dbfbb632f171)
* use default database to avoid loading default database (1688970ced90)
* extend API to make calls less verbose/to write fewer code (b91844d90a0d)

### Fix

* ensure that default value is lower equal than limit (e0e08dd68a78)

### Documentation

* describe how to use this exception (264c806d0879)

## v0.3.3

### Documentation

* update directory documentation (f4c817452652)
* add idea of default dataset (abcc494d0134)

## v0.3.2

## v0.3.0

### Feature

* add single line comment to configuration generator (2375e843f034)
* add method to generate configuration out of source (b1956694ce49)
* add first holy value concept (9c63596d980f)

### Documentation

* add release plan for increments 0.3 and 0.4 (7634978ce8f9)

## v0.2.2

## v0.1.30

## v0.1.16

### Feature

* add method to determine shared_tmp (1781a9c37633)

## v0.1.6

### Feature

* add global cache size (b3cbfa49636a)

### Documentation

* extend basic readme documentation (e4e3cff7fcc0)

## v0.1.5

### Feature

* add basic configuration for DINA4 and DINA5 pages (e932a0e7710f)

## v0.1.3

### Feature

* add export and import from viewo project (b67dcde7116b)

### Fix

* fix location to shared space (6ec668800b5b)

## v0.1.1

### Feature

* make check of path existence optional (2006e910e3df)
* add access to global folder-share environment variables (501a346a60f6)

### Fix

* add missing url to package location (21f659238feb)

## v0.1.0

### Feature

* add server from baw project (246c48abe013)

## v0.0.0 Initial release
