import { Outlet, NavLink } from 'react-router-dom';
import type { LucideIcon } from 'lucide-react';
import { LayoutDashboard, Network, FileText, Apple, BookOpen, Sparkles, PanelLeftClose, PanelLeftOpen, Activity, ChevronRight } from 'lucide-react';
import { useState } from 'react';

const NAV_ITEMS: Array<{
    to: string;
    label: string;
    subtitle: string;
    icon: LucideIcon;
}> = [
    { to: '/dashboard', label: 'Dashboard', subtitle: 'Overview and trends', icon: LayoutDashboard },
    { to: '/graph', label: 'Graph Explorer', subtitle: 'Connection map and filtering', icon: Network },
    { to: '/biomarkers', label: 'Biomarker Index', subtitle: 'Clinical marker catalog', icon: FileText },
    { to: '/foods', label: 'Food Index', subtitle: 'Evidence-backed foods', icon: Apple },
    { to: '/papers', label: 'Research Papers', subtitle: 'Linked citations', icon: BookOpen },
    { to: '/recommend', label: 'What Should I Eat?', subtitle: 'Goal-based recommendations', icon: Sparkles },
];

export default function Layout() {
    const [collapsed, setCollapsed] = useState(false);

    const navItemClass = ({ isActive }: { isActive: boolean }) =>
        `group relative flex items-center gap-3 rounded-2xl transition-all duration-200 border px-3.5 ${collapsed ? 'justify-center py-3' : 'py-3.5'} ${isActive
            ? 'bg-gradient-to-r from-cyan-500/16 to-blue-500/14 text-white border-cyan-300/30 shadow-[0_10px_25px_rgba(13,40,76,0.4)]'
            : 'text-white/82 border-transparent hover:border-white/20 hover:bg-white/[0.12] hover:text-white'}`;

    return (
        <div className="flex h-screen bg-transparent w-full overflow-hidden">
            <aside className={`flex float-up flex-col flex-shrink-0 soft-divider border-r glass-panel-strong transition-all duration-300 ${collapsed ? 'w-24' : 'w-[340px]'}`}>
                <div className={`soft-divider border-b ${collapsed ? 'px-4 py-5' : 'p-5'}`}>
                    <div className={`rounded-2xl border border-white/10 bg-white/[0.03] ${collapsed ? 'px-2.5 py-3.5' : 'px-4 py-4'}`}>
                        <div className={`flex items-center ${collapsed ? 'justify-center' : 'gap-3'}`}>
                            <div className="relative h-11 w-11 rounded-xl bg-gradient-to-br from-teal-300 via-cyan-400 to-blue-600 shadow-lg shadow-blue-500/30 flex-shrink-0">
                                <div className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-emerald-300 pulse-dot" />
                            </div>
                            {!collapsed && (
                                <div className="min-w-0">
                                    <p className="app-heading text-2xl bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-300 leading-none">BioNutri</p>
                                    <p className="text-xs uppercase tracking-[0.16em] text-cyan-200/75 mt-1">Nutrition Intelligence</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                <nav className={`flex-1 overflow-y-auto hide-scrollbar ${collapsed ? 'p-3' : 'p-4'}`}>
                    {!collapsed && (
                        <p className="px-2.5 mb-2 text-xs uppercase tracking-[0.16em] text-white/70 font-semibold">Main Views</p>
                    )}
                    <div className="space-y-2">
                        {NAV_ITEMS.map(item => {
                            const Icon = item.icon;
                            return (
                                <NavLink key={item.to} to={item.to} className={navItemClass} title={collapsed ? item.label : undefined}>
                                    {({ isActive }) => (
                                        <>
                                            <span className={`rounded-xl flex items-center justify-center transition-colors ${collapsed ? 'w-10 h-10' : 'w-11 h-11'} ${isActive
                                                ? 'bg-cyan-300/20 text-cyan-100'
                                                : 'bg-white/[0.04] text-white/55 group-hover:bg-white/10 group-hover:text-white/80'}`}>
                                                <Icon className="w-5 h-5 flex-shrink-0" />
                                            </span>
                                            {!collapsed && (
                                                <>
                                                    <span className="flex-1 min-w-0">
                                                        <span className="block text-[15px] font-semibold leading-tight">{item.label}</span>
                                                        <span className="block text-sm text-white/75 mt-0.5 truncate">{item.subtitle}</span>
                                                    </span>
                                                    <ChevronRight className={`w-4 h-4 transition-all ${isActive ? 'text-cyan-100 translate-x-0' : 'text-white/20 -translate-x-1 group-hover:text-white/45 group-hover:translate-x-0'}`} />
                                                </>
                                            )}
                                        </>
                                    )}
                                </NavLink>
                            );
                        })}
                    </div>
                </nav>

                <div className={`border-t soft-divider ${collapsed ? 'p-3 space-y-2.5' : 'p-4 space-y-3'}`}>
                    {!collapsed && (
                        <div className="glass-panel rounded-2xl px-4 py-3.5 space-y-3">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2">
                                    <Activity className="w-4 h-4 text-emerald-300" />
                                <span className="text-base text-white/90 font-medium">Dataset Status</span>
                                </div>
                                <span className="text-xs uppercase tracking-[0.12em] text-emerald-300/95 font-bold">Connected</span>
                            </div>
                            <p className="text-sm text-white/78">Use <span className="text-white">Graph Explorer</span> for filtering and <span className="text-white">What Should I Eat?</span> for ranked actions.</p>
                        </div>
                    )}
                    <button
                        onClick={() => setCollapsed(!collapsed)}
                        className={`w-full flex items-center justify-center rounded-xl transition-colors border ${collapsed ? 'h-11' : 'h-12'} text-white/55 hover:text-white border-white/10 hover:bg-white/10`}
                        title={collapsed ? 'Expand panel' : 'Collapse panel'}
                    >
                        {collapsed ? <PanelLeftOpen className="w-5 h-5" /> : <PanelLeftClose className="w-5 h-5" />}
                    </button>
                </div>
            </aside>

            <div className="flex-1 h-full overflow-hidden relative">
                <Outlet />
            </div>
        </div>
    );
}
