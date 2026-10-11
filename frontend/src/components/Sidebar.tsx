import { BookOpen, ChartNoAxesColumn, CircleHelp, FileKey2, History, LayoutDashboard, LockKeyhole, Menu, Settings2, ShieldCheck, SunMoon, X } from "lucide-react";

export type Page = "dashboard" | "workspace" | "ciphers" | "compare" | "files" | "history" | "help" | "settings";

const items: { id: Page; label: string; icon: typeof LayoutDashboard }[] = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "workspace", label: "Encrypt & decrypt", icon: LockKeyhole },
  { id: "ciphers", label: "Cipher library", icon: BookOpen },
  { id: "compare", label: "Compare algorithms", icon: ChartNoAxesColumn },
  { id: "files", label: "File operations", icon: FileKey2 },
  { id: "history", label: "Session history", icon: History },
  { id: "help", label: "Help & documentation", icon: CircleHelp },
  { id: "settings", label: "Settings", icon: Settings2 },
];

export function Sidebar({ page, onNavigate, collapsed, onToggle, onTheme }: { page: Page; onNavigate: (page: Page) => void; collapsed: boolean; onToggle: () => void; onTheme: () => void }) {
  return <aside className={`sidebar ${collapsed ? "sidebar-collapsed" : ""}`}>
    <div className="brand-row">
      <div className="brand-mark"><ShieldCheck size={19} /></div>
      {!collapsed && <div><div className="brand-name">CIPHER<span>LAB</span></div><div className="brand-caption">NETWORK SECURITY / 26–27</div></div>}
      <button className="icon-button sidebar-toggle" onClick={onToggle} aria-label="Toggle sidebar">{collapsed ? <Menu size={18} /> : <X size={18} />}</button>
    </div>
    {!collapsed && <div className="workspace-label">WORKSPACE</div>}
    <nav className="nav-list">
      {items.map(({ id, label, icon: Icon }) => <button key={id} className={`nav-item ${page === id ? "nav-item-active" : ""}`} onClick={() => onNavigate(id)} title={collapsed ? label : undefined}><Icon size={18} /><span>{!collapsed && label}</span>{page === id && !collapsed && <i />}</button>)}
    </nav>
    <div className="sidebar-footer">
      {!collapsed && <div className="notice-small"><span className="status-dot" />Educational mode active</div>}
      <button className="nav-item" onClick={onTheme} title="Toggle theme"><SunMoon size={18} /><span>{!collapsed && "Toggle theme"}</span></button>
    </div>
  </aside>;
}
