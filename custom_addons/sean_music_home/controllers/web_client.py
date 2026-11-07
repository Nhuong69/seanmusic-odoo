from odoo import http
from odoo.addons.website.controllers.backend import WebsiteBackendHome


class SeanMusicWebClient(WebsiteBackendHome):
    """Keep legacy ``/web/...`` backend URLs compatible with Website."""

    @http.route(
        "/web/<path:subpath>",
        type="http",
        auth="none",
        readonly=True,
    )
    def web_client_alias(self, subpath, **kw):
        # Preserve the path so WebsiteBackendHome can apply its website context
        # handling for Website actions before delegating to Odoo's web client.
        return super().web_client(subpath=subpath, **kw)
