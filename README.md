docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d postgres2 -u --stop-after-init
docker compose logs -f odoo

docker exec 2026-08-09-learning_odoo_docs-db-1 psql -U odoo -d postgres -c "\d estate_property"
