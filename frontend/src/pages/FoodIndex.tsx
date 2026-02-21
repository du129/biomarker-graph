import { useState, useEffect, useMemo } from 'react';
import { Search, ChevronDown, ChevronUp, TrendingUp, TrendingDown } from 'lucide-react';
import { apiUrl } from '../utils/api';

interface FoodNode {
    id: string;
    label: string;
    type: string;
    group: string;
}

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
    magnitude: string;
    summary: string;
}

const GROUP_COLORS: Record<string, { bg: string; text: string; border: string }> = {
    Grains: { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/20' },
    Protein: { bg: 'bg-red-500/10', text: 'text-red-400', border: 'border-red-500/20' },
    Fruits: { bg: 'bg-pink-500/10', text: 'text-pink-400', border: 'border-pink-500/20' },
    Vegetables: { bg: 'bg-green-500/10', text: 'text-green-400', border: 'border-green-500/20' },
    Nuts: { bg: 'bg-yellow-600/10', text: 'text-yellow-500', border: 'border-yellow-600/20' },
    Seeds: { bg: 'bg-lime-500/10', text: 'text-lime-400', border: 'border-lime-500/20' },
    Legumes: { bg: 'bg-orange-500/10', text: 'text-orange-400', border: 'border-orange-500/20' },
    Dairy: { bg: 'bg-sky-500/10', text: 'text-sky-400', border: 'border-sky-500/20' },
    Fermented: { bg: 'bg-violet-500/10', text: 'text-violet-400', border: 'border-violet-500/20' },
    Fats: { bg: 'bg-yellow-400/10', text: 'text-yellow-400', border: 'border-yellow-400/20' },
    Spices: { bg: 'bg-rose-500/10', text: 'text-rose-400', border: 'border-rose-500/20' },
    Herbs: { bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/20' },
    Beverages: { bg: 'bg-teal-500/10', text: 'text-teal-400', border: 'border-teal-500/20' },
    Treats: { bg: 'bg-fuchsia-500/10', text: 'text-fuchsia-400', border: 'border-fuchsia-500/20' },
    Condiments: { bg: 'bg-indigo-500/10', text: 'text-indigo-400', border: 'border-indigo-500/20' },
    Supplements: { bg: 'bg-cyan-500/10', text: 'text-cyan-400', border: 'border-cyan-500/20' },
    Seafood: { bg: 'bg-blue-500/10', text: 'text-blue-400', border: 'border-blue-500/20' },
    'Organ Meats': { bg: 'bg-red-600/10', text: 'text-red-500', border: 'border-red-600/20' },
    'Sea Vegetables': { bg: 'bg-teal-600/10', text: 'text-teal-500', border: 'border-teal-600/20' },
    Soy: { bg: 'bg-lime-400/10', text: 'text-lime-400', border: 'border-lime-400/20' },
};

export default function FoodIndex() {
    const [foods, setFoods] = useState<FoodNode[]>([]);
    const [allNodes, setAllNodes] = useState<NodeData[]>([]);
    const [links, setLinks] = useState<LinkData[]>([]);
    const [search, setSearch] = useState('');
    const [selectedGroup, setSelectedGroup] = useState<string | null>(null);
    const [expandedId, setExpandedId] = useState<string | null>(null);

    useEffect(() => {
        fetch(apiUrl('/graph'))
            .then(res => res.json())
            .then(data => {
                setFoods(data.nodes.filter((n: FoodNode) => n.type === 'food'));
                setAllNodes(data.nodes);
                setLinks(data.links);
            });
    }, []);

    const nodeMap = useMemo(() => {
        const m: Record<string, NodeData> = {};
        allNodes.forEach(n => { m[n.id] = n; });
        return m;
    }, [allNodes]);

    const groups = useMemo(() => {
        const g = new Set(foods.map(f => f.group));
        return Array.from(g).sort();
    }, [foods]);

    const filtered = useMemo(() => {
        return foods.filter(n => {
            const matchesSearch = n.label.toLowerCase().includes(search.toLowerCase()) || n.group.toLowerCase().includes(search.toLowerCase());
            const matchesGroup = !selectedGroup || n.group === selectedGroup;
            return matchesSearch && matchesGroup;
        });
    }, [foods, search, selectedGroup]);

    const getConnectedBiomarkers = (foodId: string) => {
        return links
            .filter(l => l.source === foodId)
            .map(l => ({
                biomarker: nodeMap[l.target],
                effect: l.effect,
                strength: l.strength,
                magnitude: l.magnitude,
                summary: l.summary,
            }))
            .filter(x => x.biomarker)
            .sort((a, b) => {
                const strengthOrder: Record<string, number> = { high: 0, medium: 1, low: 2 };
                return (strengthOrder[a.strength] ?? 3) - (strengthOrder[b.strength] ?? 3);
            });
    };

    return (
        <div className="page-shell">
            <div className="page-content">
                <div className="flex flex-col gap-6 mb-8">
                    <div>
                        <h1 className="text-4xl xl:text-5xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-teal-300 tracking-tight mb-2">Food Index</h1>
                        <p className="text-white/55 text-xl">Browse {foods.length} evidence-based foods. Click any food to see which biomarkers it affects.</p>
                    </div>
                    <div className="grid grid-cols-1 xl:grid-cols-[1.2fr_auto] gap-4 items-start">
                        <div className="relative w-full max-w-3xl">
                            <input
                                type="text"
                                placeholder="Search foods..."
                                className="toolbar-input"
                                value={search}
                                onChange={e => setSearch(e.target.value)}
                            />
                            <Search className="absolute left-4 top-4 w-5 h-5 text-white/40" />
                        </div>
                        <div className="glass-panel rounded-2xl px-5 py-3 flex items-center gap-6 text-sm">
                            <div>
                                <p className="text-white/35 uppercase text-[11px] tracking-widest">Visible</p>
                                <p className="text-white font-semibold text-lg">{filtered.length}</p>
                            </div>
                            <div>
                                <p className="text-white/35 uppercase text-[11px] tracking-widest">Groups</p>
                                <p className="text-white font-semibold text-lg">{groups.length}</p>
                            </div>
                        </div>
                    </div>
                    <div className="flex gap-2.5 flex-wrap">
                        <button
                            onClick={() => setSelectedGroup(null)}
                            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${!selectedGroup ? 'bg-blue-500/30 text-blue-200 border border-blue-400/35' : 'bg-white/5 text-white/55 border border-white/10 hover:bg-white/10'}`}
                        >
                            All Categories
                        </button>
                        {groups.map(g => (
                            <button
                                key={g}
                                onClick={() => setSelectedGroup(g === selectedGroup ? null : g)}
                                className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${g === selectedGroup ? 'bg-blue-500/30 text-blue-200 border border-blue-400/35' : 'bg-white/5 text-white/55 border border-white/10 hover:bg-white/10'}`}
                            >
                                {g}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="space-y-4">
                    {filtered.map(node => {
                        const colors = GROUP_COLORS[node.group] || { bg: 'bg-gray-500/10', text: 'text-gray-400', border: 'border-gray-500/20' };
                        const connected = getConnectedBiomarkers(node.id);
                        const isExpanded = expandedId === node.id;

                        return (
                            <div key={node.id} className={`border ${colors.border} rounded-2xl overflow-hidden transition-all duration-200`}>
                                <button
                                    onClick={() => setExpandedId(isExpanded ? null : node.id)}
                                    className={`w-full flex items-center justify-between p-6 ${colors.bg} hover:brightness-125 transition-all text-left`}
                                >
                                    <div className="flex items-center gap-4 flex-1 min-w-0">
                                        <div className={`w-3 h-3 rounded-full ${colors.text.replace('text-', 'bg-')}`} />
                                        <h3 className="font-bold text-xl text-white">{node.label}</h3>
                                    </div>
                                    <div className="flex items-center gap-4 flex-shrink-0">
                                        <span className={`text-xs uppercase tracking-wider px-2.5 py-1 rounded-full ${colors.bg} ${colors.text} font-semibold border ${colors.border}`}>
                                            {node.group}
                                        </span>
                                        <div className="flex items-center gap-2">
                                            <span className="text-white/55 text-base font-medium">{connected.length} biomarker{connected.length !== 1 ? 's' : ''}</span>
                                            {isExpanded ? <ChevronUp className="w-5 h-5 text-white/35" /> : <ChevronDown className="w-5 h-5 text-white/35" />}
                                        </div>
                                    </div>
                                </button>

                                {isExpanded && connected.length > 0 && (
                                    <div className="border-t border-white/5 bg-black/20">
                                        <div className="p-5 grid grid-cols-1 lg:grid-cols-2 gap-3">
                                            {connected.map((c, idx) => (
                                                <div key={idx} className="flex items-center gap-3 px-4 py-3 rounded-xl bg-white/[0.03] hover:bg-white/[0.06] transition-colors">
                                                    {c.effect === 'increase' ? (
                                                        <TrendingUp className="w-5 h-5 text-green-400 flex-shrink-0" />
                                                    ) : (
                                                        <TrendingDown className="w-5 h-5 text-blue-400 flex-shrink-0" />
                                                    )}
                                                    <div className="flex-1 min-w-0">
                                                        <span className="font-medium text-white/85 text-base">{c.biomarker.label}</span>
                                                        <span className="text-white/35 text-sm ml-2">{c.biomarker.group}</span>
                                                    </div>
                                                    <span className={`text-xs font-bold px-2 py-1 rounded flex-shrink-0 ${c.strength === 'high' ? 'bg-green-500/20 text-green-400' :
                                                            c.strength === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                                                                'bg-white/10 text-white/40'
                                                        }`}>
                                                        {c.strength}
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {isExpanded && connected.length === 0 && (
                                    <div className="border-t border-white/5 bg-black/20 p-6 text-center text-white/35 text-base">
                                        No biomarker connections found for this food.
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>

                {filtered.length === 0 && (
                    <div className="text-center py-20 text-white/30">
                        <p className="text-xl">No foods match your search.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
