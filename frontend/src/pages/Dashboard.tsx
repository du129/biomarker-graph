import { useEffect, useState, useMemo } from 'react';
import { Activity, Apple, Database, FileText, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { apiUrl } from '../utils/api';

interface NodeData {
    id: string;
    label: string;
    type: string;
    group: string;
}

interface LinkData {
    source: string;
    target: string;
    effect: string;
    strength: string;
    summary: string;
    citations: { title: string }[];
}

export default function Dashboard() {
    const [nodes, setNodes] = useState<NodeData[]>([]);
    const [links, setLinks] = useState<LinkData[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(apiUrl('/graph'))
            .then(res => res.json())
            .then(data => {
                setNodes(data.nodes || []);
                setLinks(data.links || []);
                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, []);

    const stats = useMemo(() => {
        const biomarkers = nodes.filter(n => n.type === 'biomarker').length;
        const foods = nodes.filter(n => n.type === 'food').length;
        const linkCount = links.length;
        const papers = new Set(links.flatMap(l => l.citations?.map(c => c.title) || [])).size;
        const highStrength = links.filter(l => l.strength === 'high').length;
        const linksWithCitations = links.filter(l => (l.citations?.length || 0) > 0).length;
        const citationCoverage = linkCount > 0 ? Math.round((linksWithCitations / linkCount) * 100) : 0;
        const foodGroups = new Set(nodes.filter(n => n.type === 'food').map(n => n.group)).size;
        const bioGroups = new Set(nodes.filter(n => n.type === 'biomarker').map(n => n.group)).size;
        const avgLinksPerBiomarker = biomarkers > 0 ? (linkCount / biomarkers).toFixed(1) : '0.0';
        const avgLinksPerFood = foods > 0 ? (linkCount / foods).toFixed(1) : '0.0';
        return { biomarkers, foods, links: linkCount, papers, highStrength, foodGroups, bioGroups, citationCoverage, avgLinksPerBiomarker, avgLinksPerFood };
    }, [nodes, links]);

    // Top connected foods
    const topFoods = useMemo(() => {
        const counts: Record<string, number> = {};
        links.forEach(l => {
            counts[l.source] = (counts[l.source] || 0) + 1;
        });
        return nodes
            .filter(n => n.type === 'food')
            .map(n => ({ ...n, count: counts[n.id] || 0 }))
            .sort((a, b) => b.count - a.count)
            .slice(0, 8);
    }, [nodes, links]);

    // Top connected biomarkers
    const topBiomarkers = useMemo(() => {
        const counts: Record<string, number> = {};
        links.forEach(l => {
            counts[l.target] = (counts[l.target] || 0) + 1;
        });
        return nodes
            .filter(n => n.type === 'biomarker')
            .map(n => ({ ...n, count: counts[n.id] || 0 }))
            .sort((a, b) => b.count - a.count)
            .slice(0, 8);
    }, [nodes, links]);

    const insightCards = useMemo(() => {
        const evidenceRatio = links.length > 0 ? Math.round((stats.highStrength / links.length) * 100) : 0;
        return [
            {
                title: 'Evidence Confidence',
                value: `${evidenceRatio}%`,
                desc: 'of links are rated high-strength evidence',
                tone: 'from-emerald-500/20 to-teal-500/10 border-emerald-400/20 text-emerald-200',
            },
            {
                title: 'Citation Coverage',
                value: `${stats.citationCoverage}%`,
                desc: 'of links include at least one source link',
                tone: 'from-blue-500/20 to-cyan-500/10 border-blue-400/20 text-blue-200',
            },
            {
                title: 'Network Density',
                value: `${stats.avgLinksPerBiomarker} / ${stats.avgLinksPerFood}`,
                desc: 'avg links per biomarker / per food',
                tone: 'from-amber-500/20 to-orange-500/10 border-amber-400/20 text-amber-200',
            },
        ];
    }, [links, stats.highStrength, stats.citationCoverage, stats.avgLinksPerBiomarker, stats.avgLinksPerFood]);

    if (loading) {
        return <div className="page-shell"><div className="page-content text-white/75">Loading dashboard data...</div></div>;
    }

    return (
        <div className="page-shell">
            <div className="page-content space-y-8 animate-in fade-in duration-500">
                <h1 className="text-4xl md:text-5xl xl:text-6xl app-heading bg-clip-text text-transparent bg-gradient-to-r from-teal-300 to-blue-400 tracking-tight">
                    Dashboard Overview
                </h1>

                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">
                    <div className="glass-panel-strong rounded-3xl p-7 hover:bg-white/14 transition-colors min-h-[170px]">
                        <div className="w-14 h-14 rounded-2xl bg-pink-500/20 flex items-center justify-center mb-5">
                            <Activity className="w-7 h-7 text-pink-400" />
                        </div>
                        <h3 className="text-4xl font-bold mb-1">{stats.biomarkers}</h3>
                        <p className="text-white/80 text-base font-medium">Biomarkers across {stats.bioGroups} categories</p>
                    </div>
                    <div className="glass-panel-strong rounded-3xl p-7 hover:bg-white/14 transition-colors min-h-[170px]">
                        <div className="w-14 h-14 rounded-2xl bg-blue-500/20 flex items-center justify-center mb-5">
                            <Apple className="w-7 h-7 text-blue-400" />
                        </div>
                        <h3 className="text-4xl font-bold mb-1">{stats.foods}</h3>
                        <p className="text-white/80 text-base font-medium">Foods across {stats.foodGroups} categories</p>
                    </div>
                    <div className="glass-panel-strong rounded-3xl p-7 hover:bg-white/14 transition-colors min-h-[170px]">
                        <div className="w-14 h-14 rounded-2xl bg-purple-500/20 flex items-center justify-center mb-5">
                            <Database className="w-7 h-7 text-purple-400" />
                        </div>
                        <h3 className="text-4xl font-bold mb-1">{stats.links}</h3>
                        <p className="text-white/80 text-base font-medium">{stats.highStrength} high-strength connections</p>
                    </div>
                    <div className="glass-panel-strong rounded-3xl p-7 hover:bg-white/14 transition-colors min-h-[170px]">
                        <div className="w-14 h-14 rounded-2xl bg-amber-500/20 flex items-center justify-center mb-5">
                            <FileText className="w-7 h-7 text-amber-400" />
                        </div>
                        <h3 className="text-4xl font-bold mb-1">{stats.papers}</h3>
                        <p className="text-white/80 text-base font-medium">Cited research papers</p>
                    </div>
                </div>

                <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
                    {insightCards.map((card) => (
                        <div key={card.title} className={`rounded-2xl border p-6 bg-gradient-to-br from-white/[0.08] to-white/[0.03] ${card.tone}`}>
                            <p className="text-sm uppercase tracking-wider text-white/80 mb-2">{card.title}</p>
                            <p className="text-2xl font-bold text-white mb-1">{card.value}</p>
                            <p className="text-base text-white/85">{card.desc}</p>
                        </div>
                    ))}
                </div>

                <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                    <div className="glass-panel-strong rounded-3xl p-7">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-2xl font-bold text-white">Most Connected Foods</h2>
                            <Link to="/foods" className="text-base text-blue-300 hover:text-blue-200 flex items-center gap-1">View all <ArrowRight className="w-4 h-4" /></Link>
                        </div>
                        <div className="space-y-3">
                            {topFoods.map((f, i) => (
                                <div key={f.id} className="flex items-center gap-4 group">
                                    <span className="text-white/55 font-mono text-sm w-5">{i + 1}</span>
                                    <div className="w-2.5 h-2.5 rounded-full bg-blue-500" />
                                    <span className="font-medium text-white/95 group-hover:text-white flex-1 transition-colors text-base">{f.label}</span>
                                    <span className="text-sm text-white/60 uppercase tracking-wider">{f.group}</span>
                                    <span className="text-blue-300 font-bold text-base">{f.count}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="glass-panel-strong rounded-3xl p-7">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-2xl font-bold text-white">Most Targeted Biomarkers</h2>
                            <Link to="/biomarkers" className="text-base text-pink-300 hover:text-pink-200 flex items-center gap-1">View all <ArrowRight className="w-4 h-4" /></Link>
                        </div>
                        <div className="space-y-3">
                            {topBiomarkers.map((b, i) => (
                                <div key={b.id} className="flex items-center gap-4 group">
                                    <span className="text-white/55 font-mono text-sm w-5">{i + 1}</span>
                                    <div className="w-2.5 h-2.5 rounded-full bg-pink-500" />
                                    <span className="font-medium text-white/95 group-hover:text-white flex-1 transition-colors text-base">{b.label}</span>
                                    <span className="text-sm text-white/60 uppercase tracking-wider">{b.group}</span>
                                    <span className="text-pink-300 font-bold text-base">{b.count}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                    <Link to="/graph" className="bg-gradient-to-br from-teal-500/12 to-blue-600/12 border border-teal-500/25 rounded-3xl p-8 hover:from-teal-500/24 hover:to-blue-600/24 transition-all group">
                        <h2 className="text-2xl font-bold mb-3 group-hover:text-teal-400 transition-colors">Graph Explorer</h2>
                        <p className="text-white/90 text-lg leading-relaxed">
                            Visualize {stats.links} connections between foods and biomarkers in an interactive force-directed graph.
                        </p>
                    </Link>
                    <Link to="/foods" className="bg-gradient-to-br from-blue-500/12 to-indigo-600/12 border border-blue-500/25 rounded-3xl p-8 hover:from-blue-500/24 hover:to-indigo-600/24 transition-all group">
                        <h2 className="text-2xl font-bold mb-3 group-hover:text-blue-400 transition-colors">Food Index</h2>
                        <p className="text-white/90 text-lg leading-relaxed">
                            Browse {stats.foods} foods across {stats.foodGroups} categories with evidence-based biomarker connections.
                        </p>
                    </Link>
                    <Link to="/papers" className="bg-gradient-to-br from-amber-500/12 to-orange-600/12 border border-amber-500/25 rounded-3xl p-8 hover:from-amber-500/24 hover:to-orange-600/24 transition-all group">
                        <h2 className="text-2xl font-bold mb-3 group-hover:text-amber-400 transition-colors">Research Papers</h2>
                        <p className="text-white/90 text-lg leading-relaxed">
                            Explore {stats.papers} cited papers from peer-reviewed journals backing every connection.
                        </p>
                    </Link>
                </div>
            </div>
        </div>
    );
}
