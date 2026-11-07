import { Component, onMounted, onWillUnmount, signal } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { router } from "@web/core/browser/router";
import { WebClient } from "@web/webclient/webclient";
import { NavBar } from "@web/webclient/navbar/navbar";

const SHORTCUTS = [];

// Odoo 20 uses /odoo as the canonical web-client prefix. Keep the client
// state and generated navigation URLs under /web for Sean Music instead.
const odooStateToUrl = router.stateToUrl;
const odooUrlToState = router.urlToState;
router.stateToUrl = (state) => odooStateToUrl(state).replace(/^\/odoo(?=\/|$)/, "/web");
router.urlToState = (url) => {
    const webUrl = new URL(url.href);
    if (webUrl.pathname === "/web" || webUrl.pathname.startsWith("/web/")) {
        webUrl.pathname = `/odoo${webUrl.pathname.slice(4)}`;
    }
    return odooUrlToState(webUrl);
};

// The router has already parsed the initial URL when this asset is loaded.
// Reparse /web/... once so the initial action is retained without exposing
// the /odoo prefix in the address bar.
if (window.location.pathname === "/web" || window.location.pathname.startsWith("/web/")) {
    const initialUrl = new URL(window.location.href);
    initialUrl.pathname = `/odoo${initialUrl.pathname.slice(4)}`;
    router.replaceState(router.urlToState(initialUrl), { replace: true, sync: true });
}

function getOdooAppIcon(menu) {
    if (menu.webIcon) {
        const [webIconClass, webIconColor, webIconBg] = menu.webIcon.split(",");
        return { webIconClass, webIconColor, webIconBg };
    }
    return { webIconClass: "apps", webIconColor: "#fff", webIconBg: "#315da4" };
}

export class SeanMusicHome extends Component {
    setup() {
        this.menu = useService("menu");
        this.query = signal("");
        const clearHomeApp = () => {
            this.menu.setCurrentMenu({ appID: null });
            sessionStorage.removeItem("menu_id");
        };
        onMounted(() => {
            // The web client restores the last selected app from sessionStorage.
            // Home is intentionally app-less, so clear that state before rendering
            // the navbar; otherwise the previous app's sections remain visible.
            clearHomeApp();
            // On a direct Home reload, WebClient can restore the previous app just
            // after this action mounts. Clear it once more after that restore pass.
            this.homeResetTimers = [0, 150].map((delay) => setTimeout(clearHomeApp, delay));
            document.body.classList.add("sean_music_home_active");
        });
        onWillUnmount(() => {
            (this.homeResetTimers || []).forEach(clearTimeout);
            document.body.classList.remove("sean_music_home_active");
        });
    }

    get displayedApps() {
        const rootApps = this.menu.getApps().map((menu) => ({
            key: `app-${menu.id}`,
            label: menu.name,
            menu,
            ...getOdooAppIcon(menu),
            webIconData: menu.webIconData,
            isApp: true,
        }));
        const shortcuts = SHORTCUTS.map((shortcut) => {
            const menu = this.menu.getAll().find((item) => item.xmlid === shortcut.xmlid);
            return menu ? { ...shortcut, key: `shortcut-${menu.id}`, menu, isApp: false } : null;
        }).filter(Boolean);
        const unique = [...rootApps, ...shortcuts].filter(
            (item, index, items) => items.findIndex((other) => other.menu.id === item.menu.id) === index
        );
        const query = this.query().trim().toLowerCase();
        return query ? unique.filter((item) => item.label.toLowerCase().includes(query)) : unique;
    }

    openMenu(menu) {
        this.menu.selectMenu(menu);
    }

    updateSearch(ev) {
        this.query.set(ev.target.value);
    }
}

SeanMusicHome.template = "sean_music_home.Home";
registry.category("actions").add("sean_music_home", SeanMusicHome);

patch(WebClient.prototype, {
    _loadDefaultApp() {
        return this.actionService.doAction("sean_music_home", { clearBreadcrumbs: true });
    },
});

patch(NavBar.prototype, {
    setup() {
        super.setup(...arguments);
        const interceptHomeMenuClick = (ev) => {
            const target = ev.target instanceof Element
                ? ev.target.closest(".o_navbar_apps_menu button[data-hotkey='h'], .o_menu_toggle")
                : null;
            if (!target) {
                return;
            }
            ev.preventDefault();
            ev.stopImmediatePropagation();
            this.openSeanMusicHome();
        };
        onMounted(() => document.addEventListener("click", interceptHomeMenuClick, true));
        onWillUnmount(() => document.removeEventListener("click", interceptHomeMenuClick, true));
    },

    openSeanMusicHome() {
        this.state.isAllAppsMenuOpened = false;
        this.state.isAppMenuSidebarOpened = false;
        this.menuService.setCurrentMenu({ appID: null });
        sessionStorage.removeItem("menu_id");
        return this.actionService.doAction("sean_music_home", { clearBreadcrumbs: true });
    },

    _openAppMenuSidebar() {
        return this.openSeanMusicHome();
    },
});
