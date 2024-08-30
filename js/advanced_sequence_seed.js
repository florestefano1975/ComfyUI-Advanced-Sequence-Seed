import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

app.registerExtension({
    name: "example.advanced_sequence_seed",
    async setup() {
        const updateSeed = (node, seed) => {
            const widget = node.widgets.find(w => w.name === "current_seed");
            if (widget) {
                widget.value = seed;
                app.graph.setDirtyCanvas(true);
            }
        };

        api.addEventListener("example.advanced_sequence_seed.update", ({ detail }) => {
            const nodes = app.graph.findNodesByType("AdvancedSequenceSeedNode");
            for (const node of nodes) {
                updateSeed(node, detail.seed);
            }
        });
    },
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "Advanced Sequence Seed Generator") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                const forceRecalcWidget = this.widgets.find(w => w.name === "force_recalculation");
                const currentSeedWidget = this.widgets.find(w => w.name === "current_seed");
                
                if (forceRecalcWidget && currentSeedWidget) {
                    forceRecalcWidget.callback = () => {
                        currentSeedWidget.disabled = forceRecalcWidget.value;
                        app.graph.setDirtyCanvas(true);
                    };
                }
                
                return result;
            };
        }
    },
});
