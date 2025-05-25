from graphviz import Digraph

def create_agile_diagram():
    # Create a new directed graph
    dot = Digraph(comment='Crop Yield Prediction System - Agile Diagram')
    dot.attr(rankdir='TB', bgcolor='white')  # Set main background to white
    
    # Style configurations
    dot.attr('node', shape='rectangle', style='rounded,filled', 
            fillcolor='white', fontname='Arial')  # Changed node background to white
    
    # Sprint 1: Data & Model Development
    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='Sprint 1: Data & Model Development', style='rounded', bgcolor='white')
        c.node('data_prep', 'Data Preparation\n- Climate Data\n- Crop Data\n- Pesticide Data')
        c.node('feat_eng', 'Feature Engineering\n- Climate Zones\n- Rainfall Zones\n- Derived Metrics')
        c.node('model_dev', 'Model Development\n- XGBoost Regressor\n- Model Training\n- Validation')
        
        c.edge('data_prep', 'feat_eng')
        c.edge('feat_eng', 'model_dev')
    
       # Sprint 2: API Development
    with dot.subgraph(name='cluster_1') as c:
        c.attr(label='Sprint 2: API Development', style='rounded', bgcolor='white')
        c.node('api_design', 'API Design\n- Endpoints\n- Data Validation\n- Error Handling')
        c.node('api_impl', 'API Implementation\n- Flask Backend\n- Model Integration\n- Response Formatting')
        c.node('api_test', 'API Testing\n- Unit Tests\n- Integration Tests\n- Performance Tests')
        
        c.edge('api_design', 'api_impl')
        c.edge('api_impl', 'api_test')
    
    # Sprint 3: Frontend Development
    with dot.subgraph(name='cluster_2') as c:
        c.attr(label='Sprint 3: Frontend Development', style='rounded', bgcolor='white')
        c.node('ui_design', 'UI Design\n- Input Forms\n- Results Display\n- Responsive Layout')
        c.node('ui_impl', 'UI Implementation\n- HTML/CSS\n- JavaScript\n- API Integration')
        c.node('ui_test', 'UI Testing\n- Browser Testing\n- Usability Testing\n- Error Scenarios')
        
        c.edge('ui_design', 'ui_impl')
        c.edge('ui_impl', 'ui_test')
    
  # Sprint 4: Deployment & Documentation
    with dot.subgraph(name='cluster_3') as c:
        c.attr(label='Sprint 4: Deployment & Documentation', style='rounded', bgcolor='white')
        c.node('deploy', 'Deployment\n- Server Setup\n- Docker Config\n- Monitoring')
        c.node('docs', 'Documentation\n- API Docs\n- User Guide\n- Technical Details')
        c.node('final_test', 'Final Testing\n- End-to-End Tests\n- Performance\n- Security')
        
        c.edge('deploy', 'docs')
        c.edge('docs', 'final_test')
    
    # Connect sprints
    dot.edge('model_dev', 'api_design')
    dot.edge('api_test', 'ui_design')
    dot.edge('ui_test', 'deploy')
    
    # Save the diagram
    dot.render('crop_predict_agile_diagram', format='png', cleanup=True)

if __name__ == '__main__':
    create_agile_diagram()