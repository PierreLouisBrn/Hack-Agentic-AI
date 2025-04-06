# tools/dynamodb_manager.py
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging

logger = logging.getLogger(__name__)

class DynamoDBManager:
    """Gestionnaire pour la table DynamoDB"""
    
    def __init__(self, table_name="sentinel", region_name="us-west-2"):
        """
        Initialise la connexion à DynamoDB
        
        Args:
            table_name: Nom de la table DynamoDB
            region_name: Région AWS
        """
        self.table_name = table_name
        self.region_name = region_name
        
        # Initialisation du client DynamoDB
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)
    
    def store_email_analysis(self, email_info, finale):
        """
        Enregistre les résultats d'analyse d'un email dans DynamoDB
        
        Args:
            email_info: Tuple (last_seen_id, subject, sender, recipient, raw_date, body_text, links)
            finale: Dictionnaire résultat avec 'is_phishing', 'summary', 'reason'
        """
        # Extraction des informations de l'email
        last_seen_id, subject, sender, recipient, raw_date, body_text, links = email_info
        
        # Construction de l'item à insérer dans DynamoDB
        item = {
            "email_id": last_seen_id,
            "subject": subject,
            "sender": sender,
            "recipient": recipient,
            "date": raw_date,
            "is_phishing": "Yes" if finale[0] else "No",
            "summary": finale[1],
            "reason": finale[2],
            "links": ", ".join(links) if links else ""
        }
        
        try:
            # Insertion dans DynamoDB
            self.table.put_item(Item=item)
            print("✅ Email enregistré dans DynamoDB.")
            return True
        except NoCredentialsError:
            print("❌ Credentials AWS manquantes.")
            return False
        except ClientError as e:
            print("❌ Erreur DynamoDB :", e.response["Error"]["Message"])
            return False