import { useState, useEffect, useMemo } from 'react';
import { Search, Sparkles, TrendingUp, TrendingDown } from 'lucide-react';
import { apiUrl } from '../utils/api';

interface NodeData { id: string; label: string; type: string; group: string; description?: string; }
interface LinkData { source: string; target: string; effect: string; strength: string; magnitude: string; timeframe: string; summary: string; citations: any[]; }

const STRENGTH_SCORE: Record<string, number> = { high: 3, medium: 2, low: 1 };

export default function Recommendations() {
    const [nodes, setNodes] = useState<NodeData[]>([]);
    const [links, setLinks] = useState<LinkData[]>([]);
    const [selectedBiomarkers, setSelectedBiomarkers] = useState<string[]>([]);
    const [goalDirection, setGoalDirection] = useState<Record<string, 'increase' | 'decrease'>>({});
    const [search, setSearch] = useState('');
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

    const biomarkers = useMemo(() => nodes.filter(n => n.type === 'biomarker'), [nodes]);
    const foods = useMemo(() => {
        const map: Record<string, NodeData> = {};
        nodes.filter(n => n.type === 'food').forEach(n => { map[n.id] = n; });
        return map;
    }, [nodes]);
    const nodeMap = useMemo(() => {
        const m: Record<string, NodeData> = {};
        nodes.forEach(n => { m[n.id] = n; });
        return m;
    }, [nodes]);

    const filteredBiomarkers = useMemo(() => {
        if (!search) return biomarkers;
        const q = search.toLowerCase();
        return biomarkers.filter(b => b.label.toLowerCase().includes(q) || b.group.toLowerCase().includes(q));
    }, [biomarkers, search]);

    const quickBiomarkers = useMemo(() => {
        const counts: Record<string, number> = {};
        links.forEach(link => {
            counts[link.target] = (counts[link.target] || 0) + 1;
        });
        return [...biomarkers]
            .sort((a, b) => (counts[b.id] || 0) - (counts[a.id] || 0))
            .slice(0, 10);
    }, [biomarkers, links]);

    const toggleBiomarker = (id: string) => {
        setSelectedBiomarkers(prev => {
            if (prev.includes(id)) return prev.filter(x => x !== id);
            return [...prev, id];
        });
    };

    const toggleDirection = (id: string) => {
        setGoalDirection(prev => ({
            ...prev,
            [id]: prev[id] === 'increase' ? 'decrease' : 'increase'
        }));
    };

    const recommendationModel = useMemo(() => {
        if (selectedBiomarkers.length === 0) return [];

        const foodScores: Record<string, {
            score: number;
            beneficialCount: number;
            conflictCount: number;
            evidenceCount: number;
            coveredBiomarkers: Set<string>;
            matches: { biomarker: string; effect: string; strength: string; magnitude: string; timeframe: string; summary: string; beneficial: boolean }[];
        }> = {};

        for (const bioId of selectedBiomarkers) {
            const desiredEffect = goalDirection[bioId] || 'decrease';
            const relevantLinks = links.filter(l => l.target === bioId);

            for (const link of relevantLinks) {
                const foodId = link.source;
                if (!foods[foodId]) continue;

                const isBeneficial = link.effect === desiredEffect;
                const strengthScore = STRENGTH_SCORE[link.strength] || 1;
                const score = isBeneficial ? strengthScore * 2.6 : -strengthScore * 1.7;

                if (!foodScores[foodId]) {
                    foodScores[foodId] = {
                        score: 0,
                        beneficialCount: 0,
                        conflictCount: 0,
                        evidenceCount: 0,
                        coveredBiomarkers: new Set<string>(),
                        matches: []
                    };
                }
                foodScores[foodId].score += score;
                foodScores[foodId].coveredBiomarkers.add(bioId);
                foodScores[foodId].evidenceCount += link.citations?.length || 0;
                if (isBeneficial) foodScores[foodId].beneficialCount += 1;
                else foodScores[foodId].conflictCount += 1;
                foodScores[foodId].matches.push({
                    biomarker: nodeMap[bioId]?.label || bioId,
                    effect: link.effect,
                    strength: link.strength,
                    magnitude: link.magnitude,
                    timeframe: link.timeframe,
                    summary: link.summary,
                    beneficial: isBeneficial,
                });
            }
        }

        return Object.entries(foodScores)
            .map(([foodId, data]) => {
                const coverageCount = data.coveredBiomarkers.size;
                const coveragePct = selectedBiomarkers.length > 0
                    ? Math.round((coverageCount / selectedBiomarkers.length) * 100)
                    : 0;
                const finalScore = data.score + coverageCount * 1.6 + Math.min(data.evidenceCount, 8) * 0.25 - data.conflictCount * 0.8;

                return {
                    food: foods[foodId],
                    finalScore,
                    coverageCount,
                    coveragePct,
                    ...data,
                };
            })
            .sort((a, b) => b.finalScore - a.finalScore);
    }, [selectedBiomarkers, goalDirection, links, foods, nodeMap]);
    const recommendations = useMemo(
        () => recommendationModel.filter(rec => rec.finalScore > 0),
        [recommendationModel]
    );
    const foodsToLimit = useMemo(
        () => recommendationModel
            .filter(rec => rec.finalScore <= 0 && rec.conflictCount > 0)
            .slice(0, 6),
        [recommendationModel]
    );
    const recommendationSummary = useMemo(() => {
        const avgCoverage = recommendations.length > 0
            ? Math.round(recommendations.reduce((acc, rec) => acc + rec.coveragePct, 0) / recommendations.length)
            : 0;
        const topEvidence = recommendations.reduce((acc, rec) => Math.max(acc, rec.evidenceCount), 0);
        return { avgCoverage, topEvidence };
    }, [recommendations]);

    if (loading) return <div className="page-shell"><div className="page-content text-white/50">Loading data...</div></div>;

    return (
        <div className="page-shell">
            <div className="page-content">
                <div className="mb-8">
                    <h1 className="text-4xl xl:text-5xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-emerald-300 to-cyan-300 tracking-tight mb-2">
                        <Sparkles className="inline w-9 h-9 mr-2 text-emerald-300" />
                        What Should I Eat?
                    </h1>
                    <p className="text-white/55 text-xl">Select biomarkers you want to improve, and get ranked food recommendations from the evidence graph.</p>
                </div>

                <div className="grid grid-cols-1 xl:grid-cols-[420px_minmax(0,1fr)] gap-6 items-start">
                    <div className="glass-panel-strong rounded-3xl p-6 xl:sticky xl:top-6">
                        <h2 className="text-sm font-bold text-white/70 mb-3 uppercase tracking-widest">Step 1 · Select Biomarkers</h2>
                        <div className="relative mb-4">
                            <input
                                type="text"
                                placeholder="Search biomarkers..."
                                className="toolbar-input"
                                value={search}
                                onChange={e => setSearch(e.target.value)}
                            />
                            <Search className="absolute left-4 top-4 w-5 h-5 text-white/40" />
                        </div>
                        <div className="flex flex-wrap gap-2 max-h-[360px] overflow-y-auto p-1">
                            {filteredBiomarkers.map(b => {
                                const selected = selectedBiomarkers.includes(b.id);
                                return (
                                    <button
                                        key={b.id}
                                        onClick={() => toggleBiomarker(b.id)}
                                        className={`px-3.5 py-2 rounded-xl text-sm font-medium transition-all border ${selected
                                            ? 'bg-emerald-500/30 text-emerald-200 border-emerald-400/45 shadow-lg shadow-emerald-500/10'
                                            : 'bg-white/5 text-white/60 border-white/10 hover:bg-white/10 hover:text-white/80'}`}
                                    >
                                        {b.label}
                                        <span className="ml-1.5 text-xs text-white/35">{b.group}</span>
                                    </button>
                                );
                            })}
                        </div>
                    </div>

                    <div className="space-y-5">
                        <div className="glass-panel rounded-3xl p-6">
                            <h2 className="text-sm font-bold text-white/70 mb-4 uppercase tracking-widest">Step 2 · Set Goals</h2>
                            {selectedBiomarkers.length === 0 ? (
                                <div className="rounded-2xl border border-dashed border-white/15 bg-white/[0.03] p-5">
                                    <p className="text-white/70 mb-3">Start with common goals:</p>
                                    <div className="flex flex-wrap gap-2">
                                        {quickBiomarkers.map((b) => (
                                            <button
                                                key={b.id}
                                                onClick={() => toggleBiomarker(b.id)}
                                                className="px-3 py-1.5 rounded-lg text-sm border border-cyan-400/25 bg-cyan-500/10 text-cyan-100 hover:bg-cyan-500/20 transition-colors"
                                            >
                                                + {b.label}
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            ) : (
                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
                                    {selectedBiomarkers.map(id => {
                                        const bio = nodeMap[id];
                                        const dir = goalDirection[id] || 'decrease';
                                        return (
                                            <div key={id} className="flex items-center justify-between bg-white/5 border border-white/10 rounded-xl px-4 py-3">
                                                <div className="flex items-center gap-2 min-w-0">
                                                    <button onClick={() => toggleBiomarker(id)} className="text-white/30 hover:text-red-400 text-xs">✕</button>
                                                    <span className="font-medium text-base text-white/85 truncate">{bio?.label}</span>
                                                </div>
                                                <button
                                                    onClick={() => toggleDirection(id)}
                                                    className={`flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-bold transition-all ${dir === 'decrease'
                                                        ? 'bg-blue-500/20 text-blue-300 border border-blue-400/30'
                                                        : 'bg-green-500/20 text-green-300 border border-green-400/30'}`}
                                                >
                                                    {dir === 'decrease' ? <TrendingDown className="w-3 h-3" /> : <TrendingUp className="w-3 h-3" />}
                                                    {dir === 'decrease' ? 'Lower' : 'Raise'}
                                                </button>
                                            </div>
                                        );
                                    })}
                                </div>
                            )}
                        </div>

                        <div className="glass-panel rounded-3xl p-6">
                            <h2 className="text-sm font-bold text-white/70 mb-4 uppercase tracking-widest">
                                Recommended Foods ({recommendations.length})
                            </h2>
                            {selectedBiomarkers.length === 0 ? (
                                <div className="text-center py-14 bg-white/5 rounded-2xl border border-dashed border-white/10">
                                    <p className="text-white/45 text-lg">Select at least one biomarker to generate recommendations.</p>
                                </div>
                            ) : recommendations.length === 0 ? (
                                <div className="text-center py-16 bg-white/5 rounded-2xl border border-dashed border-white/10">
                                    <p className="text-white/35 text-lg">No foods match your selected goals. Try flipping a direction or adding more biomarkers.</p>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-3">
                                        <div className="rounded-xl border border-white/10 bg-white/[0.03] px-4 py-3">
                                            <p className="text-[11px] text-white/40 uppercase tracking-widest">Selected Biomarkers</p>
                                            <p className="text-2xl font-bold text-white">{selectedBiomarkers.length}</p>
                                        </div>
                                        <div className="rounded-xl border border-white/10 bg-white/[0.03] px-4 py-3">
                                            <p className="text-[11px] text-white/40 uppercase tracking-widest">Avg Coverage</p>
                                            <p className="text-2xl font-bold text-cyan-200">{recommendationSummary.avgCoverage}%</p>
                                        </div>
                                        <div className="rounded-xl border border-white/10 bg-white/[0.03] px-4 py-3">
                                            <p className="text-[11px] text-white/40 uppercase tracking-widest">Max Evidence Links</p>
                                            <p className="text-2xl font-bold text-emerald-200">{recommendationSummary.topEvidence}</p>
                                        </div>
                                    </div>

                                    {recommendations.map((rec, idx) => (
                                        <div key={rec.food.id} className="bg-white/5 border border-white/10 rounded-2xl p-6 hover:bg-white/[0.07] transition-colors">
                                            <div className="flex items-start justify-between mb-4">
                                                <div className="flex items-center gap-3">
                                                    <span className={`w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold ${idx < 3 ? 'bg-emerald-500/30 text-emerald-300' : 'bg-white/10 text-white/40'}`}>
                                                        {idx + 1}
                                                    </span>
                                                    <div>
                                                        <h3 className="text-2xl font-bold text-white">{rec.food.label}</h3>
                                                        <span className="text-xs text-white/30 uppercase tracking-wider">{rec.food.group}</span>
                                                    </div>
                                                </div>
                                                <div className="flex items-center gap-2 flex-wrap justify-end">
                                                    <span className={`text-sm font-bold px-2.5 py-1 rounded-full ${rec.finalScore >= 8 ? 'bg-emerald-500/30 text-emerald-300' : rec.finalScore >= 4 ? 'bg-yellow-500/30 text-yellow-300' : 'bg-white/10 text-white/40'}`}>
                                                        Score: {Math.round(rec.finalScore)}
                                                    </span>
                                                    <span className="text-xs font-semibold px-2 py-1 rounded-full bg-cyan-500/20 text-cyan-200 border border-cyan-300/20">
                                                        Coverage {rec.coveragePct}%
                                                    </span>
                                                    <span className="text-xs font-semibold px-2 py-1 rounded-full bg-white/10 text-white/60">
                                                        Evidence {rec.evidenceCount}
                                                    </span>
                                                </div>
                                            </div>
                                            <div className="space-y-2 pl-11">
                                                {rec.matches.filter(m => m.beneficial).map((m, i) => (
                                                    <div key={i} className="flex items-start gap-2 text-sm">
                                                        <span className={`mt-0.5 ${m.effect === 'decrease' ? 'text-blue-400' : 'text-green-400'}`}>
                                                            {m.effect === 'decrease' ? '↓' : '↑'}
                                                        </span>
                                                        <div className="flex-1">
                                                            <span className="text-white/75 text-base">{m.biomarker}</span>
                                                            <span className="text-white/30 mx-1">·</span>
                                                            <span className={`text-xs font-bold px-1.5 py-0.5 rounded ${m.strength === 'high' ? 'bg-green-500/20 text-green-400' : m.strength === 'medium' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-white/10 text-white/40'}`}>
                                                                {m.strength}
                                                            </span>
                                                            <span className="text-white/30 mx-1">·</span>
                                                            <span className="text-white/45 text-sm">{m.magnitude} in {m.timeframe}</span>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>

                                            {rec.conflictCount > 0 && (
                                                <div className="mt-4 pl-11">
                                                    <p className="text-xs text-rose-200/80">
                                                        {rec.conflictCount} connection{rec.conflictCount !== 1 ? 's' : ''} may work against your selected goals.
                                                    </p>
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>

                        {foodsToLimit.length > 0 && (
                            <div className="glass-panel rounded-3xl p-6">
                                <h2 className="text-sm font-bold text-white/70 mb-4 uppercase tracking-widest">Foods To Limit For Current Goals</h2>
                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
                                    {foodsToLimit.map(rec => (
                                        <div key={rec.food.id} className="rounded-xl border border-rose-400/20 bg-rose-500/10 px-4 py-3">
                                            <div className="flex items-center justify-between">
                                                <p className="font-semibold text-rose-100">{rec.food.label}</p>
                                                <span className="text-xs text-rose-200/80">{rec.conflictCount} conflicts</span>
                                            </div>
                                            <p className="text-xs text-rose-100/70 mt-1">
                                                {rec.matches.filter(m => !m.beneficial).slice(0, 2).map(m => m.biomarker).join(', ')}
                                            </p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
