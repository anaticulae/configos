# Changelog

Every noteable change is logged here.

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
