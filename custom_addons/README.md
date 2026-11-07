# Sean Music custom addons

This directory contains custom modules for the Sean Music project. The Odoo
20 core checkout remains isolated in `odoo/` and is never modified by custom
business logic.

## Modules

- `sean_music_store`: Vietnamese storefront, inquiry form and condition fields.
- `sean_music_home`: branded login and internal home; depends on web/website only.
- `sean_music_collaborator`: install explicitly when commissions are needed.

`sean_music_collaborator` reuses Odoo Sales, Contacts and Products to provide:

- collaborator records linked to contacts;
- commission plans with a default percentage;
- product/category-specific commission rules;
- collaborator attribution on sales orders;
- commission records created on confirmation and potentially recalculated later
  (not immutable snapshots; see the project risk notes);
- product-level commission reporting.
