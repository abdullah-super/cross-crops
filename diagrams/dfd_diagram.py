from graphviz import Digraph

def create_dfd():
    """Generate a Data Flow Diagram (DFD) for the Crop Yield Prediction project."""
    dot = Digraph(comment='Crop Yield Prediction DFD', format='png')
    
    # Define nodes
    dot.node('User', 'User', shape='oval')
    dot.node('Browser', 'Web Browser', shape='oval')
    dot.node('Server', 'Flask Server\n(API)', shape='box')
    dot.node('Preproc', 'Preprocess Input', shape='box')
    dot.node('Predict', 'Predict Yield\n(ML Model)', shape='box')
    dot.node('Artifacts', 'Model & Preprocessing\nArtifacts', shape='cylinder')
    
    # Define edges
    dot.edge('User', 'Browser', label='Enters prediction form')
    dot.edge('Browser', 'Server', label='HTTP Request (/predict)')
    dot.edge('Server', 'Preproc', label='Extract & preprocess input')
    dot.edge('Preproc', 'Artifacts', label='Retrieve artifacts')
    dot.edge('Artifacts', 'Preproc', label='Provide scaler, encoders, model')
    dot.edge('Preproc', 'Predict', label='Transformed features')
    dot.edge('Predict', 'Artifacts', label='model.predict()')
    dot.edge('Artifacts', 'Predict', label='Inference result')
    dot.edge('Predict', 'Server', label='Generate prediction & interpretation')
    dot.edge('Server', 'Browser', label='HTTP Response with results')
    dot.edge('Browser', 'User', label='Display prediction')
    
    return dot

if __name__ == '__main__':
    dfd = create_dfd()
    dfd.render('crop_yield_dfd', cleanup=True)
    print("DFD diagram generated as 'crop_yield_dfd.png'.")