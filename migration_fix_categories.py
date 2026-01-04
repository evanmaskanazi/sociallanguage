"""
Migration to fix tracking categories and ensure all clients have all categories
"""
from new_backend import app, db, Client, TrackingCategory, ClientTrackingPlan

def fix_tracking_categories():
    """Ensure all clients have all tracking categories"""
    with app.app_context():
        print("Fixing tracking categories for all clients...")
        
        # Get all categories
        all_categories = TrackingCategory.query.all()
        print(f"Found {len(all_categories)} tracking categories")
        
        # Get all clients
        clients = Client.query.all()
        print(f"Found {len(clients)} clients")
        
        # For each client, ensure they have all categories
        for client in clients:
            existing_plans = {plan.category_id for plan in client.tracking_plans}
            
            for category in all_categories:
                if category.id not in existing_plans:
                    print(f"Adding category '{category.name}' to client {client.client_serial}")
                    plan = ClientTrackingPlan(
                        client_id=client.id,
                        category_id=category.id,
                        is_active=True
                    )
                    db.session.add(plan)
        
        db.session.commit()
        print("Migration complete!")

if __name__ == '__main__':
    fix_tracking_categories()