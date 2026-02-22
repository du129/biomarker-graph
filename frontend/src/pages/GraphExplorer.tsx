import { useRef, useEffect, useState, useMemo, useCallback } from 'react';
import type { ForceGraphMethods } from 'react-force-graph-2d';
import ForceGraph2D from 'react-force-graph-2d';
import type { Node, GraphData } from '../types';
import { HUD } from '../components/HUD';
import { SlidersHorizontal, Search, RotateCcw, Eye, EyeOff, Sparkles, Apple, Dna, PanelLeftClose, PanelLeftOpen } from 'lucide-react';
import { apiUrl } from '../utils/api';

/* ─── Color Palettes ────────────────────────────────────────────── */
const FOOD_GROUP_COLORS: Record<string, string> = {
    Grains: '#f59e0b', Protein: '#ef4444', Fruits: '#ec4899', Vegetables: '#22c55e',
    Nuts: '#a16207', Seeds: '#84cc16', Legumes: '#f97316', Dairy: '#38bdf8',
    Fermented: '#8b5cf6', Fats: '#eab308', Spices: '#fb7185', Herbs: '#34d399',
    Beverages: '#14b8a6', Treats: '#d946ef', Condiments: '#818cf8', Supplements: '#06b6d4',
    Seafood: '#3b82f6', 'Organ Meats': '#b91c1c', 'Sea Vegetables': '#0d9488', Soy: '#a3e635',
};

const BIO_GROUP_COLORS: Record<string, string> = {
    Hematology: '#f87171', Immune: '#facc15', Metabolic: '#fb923c', Kidney: '#a78bfa',
    Electrolytes: '#22d3ee', 'Bone/Mineral': '#a8a29e', Minerals: '#2dd4bf', Liver: '#4ade80',
    Lipids: '#fbbf24', Inflammation: '#f43f5e', Cardiovascular: '#f472b6', Thyroid: '#a78bfa',
    Vitamins: '#a3e635', Hormones: '#e879f9', 'Iron/Anemia': '#ef4444', 'General Health': '#38bdf8',
};

function getNodeColor(node: Node): string {
    if (node.type === 'food') return FOOD_GROUP_COLORS[node.group] || '#3b82f6';
    return BIO_GROUP_COLORS[node.group] || '#ef4444';
}

/* ─── Component ──────────────────────────────────────────────────── */
export default function GraphExplorer() {
    const graphRef = useRef<ForceGraphMethods | undefined>(undefined);
    const [data, setData] = useState<GraphData>({ nodes: [], links: [] });
    const [dimensions, setDimensions] = useState({ w: 0, h: 0 });
    const [isLoading, setIsLoading] = useState(true);
    const [fetchError, setFetchError] = useState<string | null>(null);
    const [selectedNode, setSelectedNode] = useState<Node | null>(null);
    const [hoveredNode, setHoveredNode] = useState<string | null>(null);
    const [filterType, setFilterType] = useState<'all' | 'food' | 'biomarker'>('all');
    const [filterGroup, setFilterGroup] = useState<string | null>(null);
    const [showLabels, setShowLabels] = useState(true);
    const [groupSearch, setGroupSearch] = useState('');
    const [controlsCollapsed, setControlsCollapsed] = useState(true);

    /* ── Data fetch + resize ───────────────────────────────────── */
    useEffect(() => {
        const container = document.getElementById('graph-container');
        if (!container) return;
        setDimensions({ w: container.clientWidth, h: container.clientHeight });
        const ro = new ResizeObserver(entries => {
            for (const entry of entries) {
                setDimensions({ w: entry.contentRect.width, h: entry.contentRect.height });
            }
        });
        ro.observe(container);
        fetch(apiUrl('/graph'))
            .then(r => r.json())
            .then((graphData) => {
                setData(graphData);
                setFetchError(null);
            })
            .catch((err) => {
                console.error('Failed to fetch graph data:', err);
                setFetchError('Unable to load graph data');
            })
            .finally(() => setIsLoading(false));
        return () => ro.disconnect();
    }, []);

    /* ── Physics ───────────────────────────────────────────────── */
    useEffect(() => {
        if (data.nodes.length > 0 && dimensions.w > 0 && graphRef.current) {
            graphRef.current.d3Force('charge')?.strength(-400);
            graphRef.current.d3Force('link')?.distance(90);
            graphRef.current.d3Force('center')?.strength(0.2);
            graphRef.current.d3ReheatSimulation();
            setTimeout(() => graphRef.current?.zoomToFit(800, 60), 300);
        }
    }, [data, dimensions.w, dimensions.h]);

    /* ── Derived sets for focus mode ──────────────────────────── */
    const neighborIds = useMemo(() => {
        if (!selectedNode) return new Set<string>();
        const ids = new Set<string>();
        ids.add(selectedNode.id);
        data.links.forEach((l: any) => {
            const sid = typeof l.source === 'object' ? l.source.id : l.source;
            const tid = typeof l.target === 'object' ? l.target.id : l.target;
            if (sid === selectedNode.id) ids.add(tid);
            if (tid === selectedNode.id) ids.add(sid);
        });
        return ids;
    }, [selectedNode, data.links]);

    const hoveredNeighborIds = useMemo(() => {
        if (!hoveredNode || selectedNode) return new Set<string>();
        const ids = new Set<string>();
        ids.add(hoveredNode);
        data.links.forEach((l: any) => {
            const sid = typeof l.source === 'object' ? l.source.id : l.source;
            const tid = typeof l.target === 'object' ? l.target.id : l.target;
            if (sid === hoveredNode) ids.add(tid);
            if (tid === hoveredNode) ids.add(sid);
        });
        return ids;
    }, [hoveredNode, selectedNode, data.links]);

    /* ── Connectivity count for node sizing ───────────────────── */
    const connectivityMap = useMemo(() => {
        const m: Record<string, number> = {};
        data.links.forEach((l: any) => {
            const sid = typeof l.source === 'object' ? l.source.id : l.source;
            const tid = typeof l.target === 'object' ? l.target.id : l.target;
            m[sid] = (m[sid] || 0) + 1;
            m[tid] = (m[tid] || 0) + 1;
        });
        return m;
    }, [data.links]);

    /* ── Filtered data ────────────────────────────────────────── */
    const filteredData = useMemo(() => {
        // If no filter, show everything
        if (filterType === 'all' && !filterGroup) return data;

        // Step 1: Get the primary filtered nodes
        let primaryNodes = data.nodes;
        if (filterType !== 'all') primaryNodes = primaryNodes.filter(n => n.type === filterType);
        if (filterGroup) primaryNodes = primaryNodes.filter(n => n.group === filterGroup);
        const primaryIds = new Set(primaryNodes.map(n => n.id));

        // Step 2: Find all links that touch a primary node
        const relevantLinks = data.links.filter((l: any) => {
            const sid = typeof l.source === 'object' ? l.source.id : l.source;
            const tid = typeof l.target === 'object' ? l.target.id : l.target;
            return primaryIds.has(sid) || primaryIds.has(tid);
        });

        // Step 3: Collect neighbor node IDs (so we see the *connected* nodes too)
        const neighborIds = new Set<string>();
        relevantLinks.forEach((l: any) => {
            const sid = typeof l.source === 'object' ? l.source.id : l.source;
            const tid = typeof l.target === 'object' ? l.target.id : l.target;
            neighborIds.add(sid);
            neighborIds.add(tid);
        });

        // Step 4: Build the full node set (primary + neighbors)
        const allIds = new Set([...primaryIds, ...neighborIds]);
        const nodes = data.nodes.filter(n => allIds.has(n.id));

        return { nodes, links: relevantLinks };
    }, [data, filterType, filterGroup]);

    /* ── Group lists ──────────────────────────────────────────── */
    const foodGroups = useMemo(() => [...new Set(data.nodes.filter(n => n.type === 'food').map(n => n.group))].sort(), [data.nodes]);
    const bioGroups = useMemo(() => [...new Set(data.nodes.filter(n => n.type === 'biomarker').map(n => n.group))].sort(), [data.nodes]);
    const foodGroupCounts = useMemo(() => {
        const counts: Record<string, number> = {};
        data.nodes.forEach((node) => {
            if (node.type === 'food') counts[node.group] = (counts[node.group] || 0) + 1;
        });
        return counts;
    }, [data.nodes]);
    const bioGroupCounts = useMemo(() => {
        const counts: Record<string, number> = {};
        data.nodes.forEach((node) => {
            if (node.type === 'biomarker') counts[node.group] = (counts[node.group] || 0) + 1;
        });
        return counts;
    }, [data.nodes]);
    const topFoods = useMemo(
        () => data.nodes
            .filter(n => n.type === 'food')
            .sort((a, b) => (connectivityMap[b.id] || 0) - (connectivityMap[a.id] || 0))
            .slice(0, 3),
        [data.nodes, connectivityMap]
    );
    const topBiomarkers = useMemo(
        () => data.nodes
            .filter(n => n.type === 'biomarker')
            .sort((a, b) => (connectivityMap[b.id] || 0) - (connectivityMap[a.id] || 0))
            .slice(0, 3),
        [data.nodes, connectivityMap]
    );
    const filteredFoodGroups = useMemo(
        () => foodGroups.filter(g => g.toLowerCase().includes(groupSearch.toLowerCase())),
        [foodGroups, groupSearch]
    );
    const filteredBioGroups = useMemo(
        () => bioGroups.filter(g => g.toLowerCase().includes(groupSearch.toLowerCase())),
        [bioGroups, groupSearch]
    );
    const visibleFoods = useMemo(
        () => filteredData.nodes.filter(n => n.type === 'food').length,
        [filteredData.nodes]
    );
    const visibleBiomarkers = useMemo(
        () => filteredData.nodes.filter(n => n.type === 'biomarker').length,
        [filteredData.nodes]
    );

    /* ── Selected links for HUD ───────────────────────────────── */
    const selectedLinks = useMemo(() => {
        if (!selectedNode) return [];
        return data.links.filter((link: any) =>
            (typeof link.source === 'object' ? link.source.id : link.source) === selectedNode.id ||
            (typeof link.target === 'object' ? link.target.id : link.target) === selectedNode.id
        );
    }, [selectedNode, data.links]);

    /* ── Handlers ─────────────────────────────────────────────── */
    const handleNodeClick = useCallback((node: any) => {
        setSelectedNode(node);
        graphRef.current?.centerAt(node.x, node.y, 600);
        graphRef.current?.zoom(3.5, 800);
    }, []);

    const handleSearch = useCallback((query: string) => {
        const node = data.nodes.find(n => n.label.toLowerCase() === query.toLowerCase());
        if (node) handleNodeClick(node);
    }, [data.nodes, handleNodeClick]);

    const resetView = useCallback(() => {
        setSelectedNode(null);
        setHoveredNode(null);
        setFilterType('all');
        setFilterGroup(null);
        setTimeout(() => graphRef.current?.zoomToFit(600, 60), 50);
    }, []);

    /* ── Canvas rendering ─────────────────────────────────────── */
    const nodeCanvasObject = useCallback((node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
        const color = getNodeColor(node);
        const isFocused = selectedNode != null;
        const isNeighbor = neighborIds.has(node.id);
        const isHovNeighbor = hoveredNeighborIds.has(node.id);
        const isSelected = selectedNode?.id === node.id;
        const isHovered = hoveredNode === node.id;

        // Determine opacity
        let alpha = 1;
        if (isFocused && !isNeighbor) alpha = 0.06;
        else if (hoveredNode && !selectedNode && !isHovNeighbor) alpha = 0.12;

        // Node size based on connectivity
        const count = connectivityMap[node.id] || 1;
        const baseR = Math.min(3 + count * 0.8, 12);
        const r = isSelected ? baseR + 3 : isHovered ? baseR + 2 : baseR;

        // Glow for selected / hovered
        if (isSelected || isHovered) {
            ctx.beginPath();
            ctx.arc(node.x, node.y, r + 4, 0, 2 * Math.PI);
            const grad = ctx.createRadialGradient(node.x, node.y, r, node.x, node.y, r + 6);
            grad.addColorStop(0, color + '60');
            grad.addColorStop(1, color + '00');
            ctx.fillStyle = grad;
            ctx.fill();
        }

        // Outer ring for selected
        if (isSelected) {
            ctx.beginPath();
            ctx.arc(node.x, node.y, r + 2, 0, 2 * Math.PI);
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1.5 / globalScale;
            ctx.stroke();
        }

        // Core circle
        ctx.beginPath();
        ctx.arc(node.x, node.y, r, 0, 2 * Math.PI);
        ctx.globalAlpha = alpha;

        // Food = filled circle, Biomarker = outlined diamond-like
        if (node.type === 'food') {
            ctx.fillStyle = color;
            ctx.fill();
        } else {
            ctx.fillStyle = color + '30';
            ctx.fill();
            ctx.strokeStyle = color;
            ctx.lineWidth = 1.5 / globalScale;
            ctx.stroke();
        }

        // Label logic: show if labels on & (selected/hovered/neighbor when focused) or always if zoomed in
        const showThisLabel = showLabels && (
            isSelected || isHovered ||
            (isFocused && isNeighbor) ||
            (!isFocused && !hoveredNode && globalScale > 1.8) ||
            (!isFocused && isHovNeighbor)
        );

        if (showThisLabel) {
            const fontSize = isSelected ? 13 / globalScale : 11 / globalScale;
            ctx.font = `${isSelected ? '700' : '500'} ${fontSize}px Inter, system-ui, sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'top';

            const text = node.label;
            const tw = ctx.measureText(text).width;
            const pad = 3 / globalScale;
            const labelY = node.y + r + 3 / globalScale;

            // Background pill
            ctx.fillStyle = 'rgba(0,0,0,0.75)';
            ctx.globalAlpha = alpha;
            const bx = node.x - tw / 2 - pad;
            const by = labelY - pad / 2;
            const bw = tw + pad * 2;
            const bh = fontSize + pad;
            const br = 3 / globalScale;
            ctx.beginPath();
            ctx.roundRect(bx, by, bw, bh, br);
            ctx.fill();

            // Text
            ctx.fillStyle = isSelected ? '#ffffff' : 'rgba(255,255,255,0.85)';
            ctx.fillText(text, node.x, labelY);
        }

        ctx.globalAlpha = 1;
    }, [selectedNode, hoveredNode, neighborIds, hoveredNeighborIds, connectivityMap, showLabels]);

    const linkCanvasObject = useCallback((link: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
        const sid = typeof link.source === 'object' ? link.source.id : link.source;
        const tid = typeof link.target === 'object' ? link.target.id : link.target;
        const isFocused = selectedNode != null;
        const isActiveLink = isFocused && (neighborIds.has(sid) && neighborIds.has(tid) && (sid === selectedNode?.id || tid === selectedNode?.id));
        const isHovLink = !selectedNode && hoveredNode != null && (sid === hoveredNode || tid === hoveredNode);

        let alpha = 0.12;
        if (isActiveLink) alpha = 0.9;
        else if (isHovLink) alpha = 0.6;
        else if (isFocused) alpha = 0.025;
        else if (hoveredNode) alpha = 0.04;

        const sx = link.source.x ?? 0;
        const sy = link.source.y ?? 0;
        const tx = link.target.x ?? 0;
        const ty = link.target.y ?? 0;

        ctx.beginPath();
        ctx.moveTo(sx, sy);

        // Slight curve for visual separation
        const midX = (sx + tx) / 2;
        const midY = (sy + ty) / 2;
        const dx = tx - sx;
        const dy = ty - sy;
        const curvature = 0.15;
        const cpx = midX + dy * curvature;
        const cpy = midY - dx * curvature;
        ctx.quadraticCurveTo(cpx, cpy, tx, ty);

        const lineColor = link.effect === 'increase' ? '#4ade80' : '#60a5fa';
        ctx.strokeStyle = lineColor;
        ctx.globalAlpha = alpha;
        ctx.lineWidth = (isActiveLink ? 2.5 : isHovLink ? 2 : 1) / globalScale;
        ctx.stroke();

        // Strength dot at midpoint for active links
        if (isActiveLink && link.strength === 'high') {
            const dotX = cpx;
            const dotY = cpy;
            ctx.beginPath();
            ctx.arc(dotX, dotY, 2 / globalScale, 0, 2 * Math.PI);
            ctx.fillStyle = lineColor;
            ctx.globalAlpha = 0.8;
            ctx.fill();
        }

        ctx.globalAlpha = 1;
    }, [selectedNode, hoveredNode, neighborIds]);

    return (
        <div className="relative w-full h-full overflow-hidden" id="graph-container">
            {controlsCollapsed ? (
                <div className="absolute top-2 left-2 md:top-4 md:left-4 z-30 w-[72px] pointer-events-auto">
                    <div className="glass-panel-strong rounded-2xl p-2.5 flex flex-col items-center gap-2.5">
                        <button
                            onClick={() => setControlsCollapsed(false)}
                            className="w-full h-11 rounded-xl bg-white/10 hover:bg-white/15 border border-white/10 text-white/80 flex items-center justify-center transition-colors"
                            title="Expand controls"
                        >
                            <PanelLeftOpen className="w-4 h-4" />
                        </button>
                        <button
                            onClick={() => setShowLabels(!showLabels)}
                            className="w-full h-11 rounded-xl hover:bg-white/10 text-white/60 hover:text-white/90 transition-colors flex items-center justify-center"
                            title={showLabels ? 'Hide labels' : 'Show labels'}
                        >
                            {showLabels ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                        </button>
                        <button
                            onClick={resetView}
                            className="w-full h-11 rounded-xl hover:bg-white/10 text-white/60 hover:text-white/90 transition-colors flex items-center justify-center"
                            title="Reset view"
                        >
                            <RotateCcw className="w-4 h-4" />
                        </button>
                        <div className="w-full rounded-xl border border-white/10 bg-white/[0.03] px-2 py-2.5 text-xs text-white/65 text-center leading-tight">
                            {filteredData.nodes.length} nodes
                            <br />
                            {filteredData.links.length} links
                        </div>
                    </div>
                </div>
            ) : (
                <div className="absolute top-2 left-2 right-2 md:top-4 md:left-4 md:right-auto z-30 md:w-[min(350px,calc(100vw-2rem))] h-[64vh] max-h-[540px] md:h-[min(82dvh,700px)] pointer-events-auto">
                    <div className="glass-panel-strong rounded-3xl h-full p-3.5 md:p-4 flex flex-col">
                        <div className="rounded-2xl border border-white/12 bg-white/[0.03] px-3 py-3">
                            <div className="flex items-start justify-between">
                                <div>
                                    <p className="text-xs uppercase tracking-[0.14em] text-cyan-200/85 font-semibold mb-1">Graph HUD</p>
                                    <p className="text-white text-lg font-semibold leading-tight">Navigation & Filters</p>
                                </div>
                                <button
                                    onClick={() => setControlsCollapsed(true)}
                                    className="h-11 w-11 rounded-xl bg-white/[0.04] hover:bg-white/[0.11] text-white/70 hover:text-white transition-colors flex items-center justify-center border border-white/10"
                                    title="Collapse controls"
                                >
                                    <PanelLeftClose className="w-4 h-4" />
                                </button>
                            </div>
                            <div className="mt-3 grid grid-cols-3 gap-1.5">
                                <div className="rounded-xl border border-white/10 bg-black/20 px-2.5 py-2">
                                    <p className="text-xs uppercase tracking-[0.12em] text-white/55">Foods</p>
                                    <p className="text-sm font-semibold text-white/90">{visibleFoods}</p>
                                </div>
                                <div className="rounded-xl border border-white/10 bg-black/20 px-2.5 py-2">
                                    <p className="text-xs uppercase tracking-[0.12em] text-white/55">Biomarkers</p>
                                    <p className="text-sm font-semibold text-white/90">{visibleBiomarkers}</p>
                                </div>
                                <div className="rounded-xl border border-white/10 bg-black/20 px-2.5 py-2">
                                    <p className="text-xs uppercase tracking-[0.12em] text-white/55">Links</p>
                                    <p className="text-sm font-semibold text-white/90">{filteredData.links.length}</p>
                                </div>
                            </div>
                        </div>

                        <div className="mt-2.5 grid grid-cols-2 gap-2">
                            <button
                                onClick={() => setShowLabels(!showLabels)}
                                className="rounded-xl px-2.5 py-2 text-xs bg-white/[0.04] border border-white/10 text-white/75 hover:text-white hover:bg-white/10 transition-colors flex items-center justify-center gap-1.5"
                            >
                                {showLabels ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                                {showLabels ? 'Labels On' : 'Labels Off'}
                            </button>
                            <button
                                onClick={resetView}
                                className="rounded-xl px-2.5 py-2 text-xs bg-white/[0.04] border border-white/10 text-white/75 hover:text-white hover:bg-white/10 transition-colors flex items-center justify-center gap-1.5"
                            >
                                <RotateCcw className="w-4 h-4" />
                                Reset View
                            </button>
                        </div>

                        <section className="mt-3 rounded-2xl border border-white/10 bg-white/[0.02] p-3 flex-1 min-h-0 flex flex-col">
                            <p className="text-xs uppercase tracking-[0.14em] text-white/55 font-bold mb-2">View Mode</p>
                            <div className="grid grid-cols-3 gap-2">
                                {([
                                    { key: 'all', label: 'All', icon: SlidersHorizontal },
                                    { key: 'food', label: 'Foods', icon: Apple },
                                    { key: 'biomarker', label: 'Bio', icon: Dna },
                                ] as const).map(option => {
                                    const Icon = option.icon;
                                    const active = filterType === option.key;
                                    return (
                                        <button
                                            key={option.key}
                                            onClick={() => { setFilterType(option.key); setFilterGroup(null); setSelectedNode(null); }}
                                            className={`rounded-xl px-2 py-2 text-xs font-semibold flex items-center justify-center gap-1.5 transition-all border ${active
                                                ? 'bg-cyan-500/18 text-cyan-100 border-cyan-300/30'
                                                : 'bg-white/[0.04] text-white/55 border-white/10 hover:bg-white/10 hover:text-white/85'}`}
                                        >
                                            <Icon className="w-4 h-4" />
                                            <span>{option.label}</span>
                                        </button>
                                    );
                                })}
                            </div>

                            <div className="relative mt-3">
                                <input
                                    value={groupSearch}
                                    onChange={(e) => setGroupSearch(e.target.value)}
                                    placeholder="Search categories..."
                                    className="w-full rounded-xl bg-white/[0.04] border border-white/10 py-2 pl-8 pr-3 text-sm text-white placeholder-white/45 focus:outline-none focus:border-cyan-400/40"
                                />
                                <Search className="absolute left-3 top-3 w-4 h-4 text-white/35" />
                            </div>

                            <button
                                onClick={() => { setFilterGroup(null); setSelectedNode(null); }}
                                className={`mt-2.5 w-full rounded-xl px-3 py-2 text-left text-sm transition-all border ${!filterGroup
                                    ? 'bg-white/12 border-white/25 text-white font-semibold'
                                    : 'bg-white/[0.04] border-white/10 text-white/60 hover:bg-white/10 hover:text-white/85'}`}
                            >
                                Show All Categories
                            </button>

                            <div className="mt-3 min-h-0 flex-1 overflow-y-auto hide-scrollbar pr-1 space-y-2.5">
                                {(filterType === 'all' || filterType === 'food') && (
                                    <div className="space-y-1.5">
                                        <p className="text-xs uppercase tracking-[0.12em] text-blue-200/80 font-semibold px-1">Food Groups</p>
                                        <div className="max-h-48 overflow-y-auto hide-scrollbar pr-1 space-y-1.5">
                                            {filteredFoodGroups.map(g => (
                                                <button
                                                    key={g}
                                                    onClick={() => { setFilterGroup(g === filterGroup ? null : g); setSelectedNode(null); }}
                                                    className={`w-full rounded-lg px-2.5 py-2 text-sm text-left transition-all border flex items-center gap-2 ${g === filterGroup
                                                        ? 'bg-blue-500/20 border-blue-300/35 text-blue-100'
                                                        : 'bg-white/[0.04] border-white/10 text-white/65 hover:bg-white/10 hover:text-white/85'}`}
                                                >
                                                    <span className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: FOOD_GROUP_COLORS[g] || '#888' }} />
                                                    <span className="truncate flex-1">{g}</span>
                                                    <span className="text-xs rounded-md border border-white/15 bg-black/25 px-1.5 py-0.5 text-white/60">{foodGroupCounts[g] || 0}</span>
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {(filterType === 'all' || filterType === 'biomarker') && (
                                    <div className="space-y-1.5">
                                        <p className="text-xs uppercase tracking-[0.12em] text-rose-200/80 font-semibold px-1">Biomarker Groups</p>
                                        {filteredBioGroups.map(g => (
                                            <button
                                                key={g}
                                                onClick={() => { setFilterGroup(g === filterGroup ? null : g); setSelectedNode(null); }}
                                                className={`w-full rounded-lg px-2.5 py-2 text-sm text-left transition-all border flex items-center gap-2 ${g === filterGroup
                                                    ? 'bg-rose-500/20 border-rose-300/35 text-rose-100'
                                                    : 'bg-white/[0.04] border-white/10 text-white/65 hover:bg-white/10 hover:text-white/85'}`}
                                            >
                                                <span className="w-2.5 h-2.5 rounded-sm flex-shrink-0" style={{ backgroundColor: BIO_GROUP_COLORS[g] || '#888' }} />
                                                <span className="truncate flex-1">{g}</span>
                                                <span className="text-xs rounded-md border border-white/15 bg-black/25 px-1.5 py-0.5 text-white/60">{bioGroupCounts[g] || 0}</span>
                                            </button>
                                        ))}
                                    </div>
                                )}

                                {(filteredFoodGroups.length === 0 && filteredBioGroups.length === 0) && (
                                    <div className="rounded-xl border border-dashed border-white/15 bg-white/[0.02] px-3 py-4 text-center text-sm text-white/45">
                                        No categories match your search.
                                    </div>
                                )}
                            </div>
                        </section>

                        <section className="mt-3 rounded-2xl border border-white/10 bg-white/[0.03] px-3 py-2.5">
                            <p className="text-xs uppercase tracking-[0.14em] text-white/55 font-bold mb-2">Quick Focus</p>
                            <div className="grid grid-cols-2 gap-2">
                                <div className="space-y-1.5">
                                    <p className="text-xs uppercase tracking-[0.1em] text-blue-200/80 font-semibold">Foods</p>
                                    {topFoods.map(node => (
                                        <button
                                            key={node.id}
                                            onClick={() => handleNodeClick(node)}
                                            className="w-full px-2.5 py-1.5 text-xs rounded-lg bg-blue-500/15 border border-blue-300/25 text-blue-100 hover:bg-blue-500/25 transition-colors text-left"
                                        >
                                            {node.label}
                                        </button>
                                    ))}
                                </div>
                                <div className="space-y-1.5">
                                    <p className="text-xs uppercase tracking-[0.1em] text-rose-200/80 font-semibold">Biomarkers</p>
                                    {topBiomarkers.map(node => (
                                        <button
                                            key={node.id}
                                            onClick={() => handleNodeClick(node)}
                                            className="w-full px-2.5 py-1.5 text-xs rounded-lg bg-rose-500/15 border border-rose-300/25 text-rose-100 hover:bg-rose-500/25 transition-colors text-left"
                                        >
                                            {node.label}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            <div className="mt-2.5 rounded-xl bg-black/20 border border-white/10 px-3 py-2 text-xs text-white/70 flex items-center justify-between">
                                <span className="flex items-center gap-1.5">
                                    <Sparkles className="w-4 h-4 text-cyan-200/80" />
                                    Active View
                                </span>
                                <span className="font-semibold text-white/90">{filterGroup ?? 'All categories'}</span>
                            </div>
                        </section>
                    </div>
                </div>
            )}

            {/* ── HUD (search + detail) ──────────────────────── */}
            <HUD
                selectedNode={selectedNode}
                selectedLinks={selectedLinks}
                onClose={() => { setSelectedNode(null); setTimeout(() => graphRef.current?.zoomToFit(600, 60), 50); }}
                onSearch={handleSearch}
                graphData={data}
                leftPanelCollapsed={controlsCollapsed}
            />

            {/* ── Graph canvas ───────────────────────────────── */}
            {dimensions.w > 0 && (
                <ForceGraph2D
                    ref={graphRef}
                    width={dimensions.w}
                    height={dimensions.h}
                    graphData={filteredData}
                    backgroundColor="rgba(0,0,0,0)"

                    // Physics
                    d3VelocityDecay={0.35}
                    d3AlphaDecay={0.025}
                    cooldownTicks={150}
                    onEngineStop={() => graphRef.current?.zoomToFit(400, 60)}

                    // Interactions
                    onNodeClick={handleNodeClick}
                    onNodeHover={(node: any) => setHoveredNode(node?.id || null)}
                    onBackgroundClick={() => { setSelectedNode(null); setHoveredNode(null); }}

                    // Custom rendering
                    nodeCanvasObject={nodeCanvasObject}
                    nodePointerAreaPaint={(node: any, color, ctx) => {
                        const count = connectivityMap[node.id] || 1;
                        const r = Math.min(3 + count * 0.8, 12) + 4;
                        ctx.fillStyle = color;
                        ctx.beginPath();
                        ctx.arc(node.x, node.y, r, 0, 2 * Math.PI);
                        ctx.fill();
                    }}

                    linkCanvasObject={linkCanvasObject}
                    linkCanvasObjectMode={() => 'replace'}
                />
            )}

            {isLoading && (
                <div className="absolute inset-0 z-10 flex items-center justify-center pointer-events-none">
                    <div className="glass-panel rounded-2xl px-5 py-3 text-sm text-white/65">Loading graph intelligence...</div>
                </div>
            )}
            {!isLoading && fetchError && (
                <div className="absolute inset-0 z-10 flex items-center justify-center pointer-events-none">
                    <div className="glass-panel rounded-2xl px-5 py-3 text-sm text-rose-200/90">{fetchError}</div>
                </div>
            )}
        </div>
    );
}
