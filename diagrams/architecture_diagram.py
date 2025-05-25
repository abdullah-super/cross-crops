from graphviz import Digraph

def create_architecture_diagram():
    """Generate an Architecture Diagram for the Crop Yield Prediction project with vertical layout."""
    dot = Digraph('Architecture Diagram', format='png')
    # Change layout to top-to-bottom instead of left-to-right.
    dot.attr(rankdir='TB', fontsize='10')
    
    # Frontend cluster
    with dot.subgraph(name='cluster_frontend') as f:
        f.attr(label='Frontend', color='blue', style='rounded')
        f.node('User', 'User', shape='oval')
        f.node('Browser', 'Web Browser\n(UI: index.html)')
        f.edge('User', 'Browser', label='Interacts with')
    
    # Backend cluster
    with dot.subgraph(name='cluster_backend') as b:
        b.attr(label='Backend (Flask Server)', color='red', style='rounded')
        b.node('Server', 'Flask Server\n(API Endpoints: /, /predict, /api/info, /health)')
        b.node('Preprocess', 'preprocess_input()')
        b.node('Predict', 'model.predict()\nget_yield_interpretation()')
        # Flow inside backend
        b.edge('Server', 'Preprocess', label='Process Request')
        b.edge('Preprocess', 'Predict', label='Transform Features')
        b.edge('Predict', 'Server', label='Return Prediction')
    
    # Model Artifacts cluster
    with dot.subgraph(name='cluster_model') as m:
        m.attr(label='Model Artifacts', color='green', style='rounded')
        m.node('Artifacts', 'Model & Preprocessing\nArtifacts\n(model, scaler, encoders)')
        # Connection between backend and model artifacts shown using dashed edges
        dot.edge('Preprocess', 'Artifacts', label='Load Artifacts', style='dashed')
        dot.edge('Artifacts', 'Preprocess', label='Provide scaler,\nencoders & model', style='dashed')
    
    # Connection between Frontend and Backend
    dot.edge('Browser', 'Server', label='HTTP Request (/predict)')
    dot.edge('Server', 'Browser', label='HTTP Response with JSON')
    
    return dot

if __name__ == '__main__':
    diagram = create_architecture_diagram()
    diagram.render('crop_yield_architecture_diagram', cleanup=True)
    print("Architecture diagram generated as 'crop_yield_architecture_diagram.png'.")