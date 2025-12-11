import Openregister from 'openregister';
import 'dotenv/config';
import fs from 'fs';

const client = new Openregister({
apiKey: process.env.OPEN_REGISTER_API_KEY,
});

const company_ids = ['DE-HRB-M1201-128843', 'DE-HRB-M1201-43507'];
const document_categories = ["current_printout", "chronological_printout", "historical_printout", "structured_information", "shareholder_list", "articles_of_association"]

for (const company_id of company_ids) {
    for (const document_category of document_categories) {
        try 
        {
            const response = await client.document.getRealtimeV1({
                company_id: company_id,
                document_category: document_category,
            });

            const output = JSON.stringify(response, null, 2);
            
            const title = `openregister_${document_category}`;
            const filename = `${title}_${company_id}.txt`;
        
            fs.writeFileSync(filename, output);
        }
        catch(error)
        {
            console.log(`No document found for company_id: ${company_id} with category: ${document_category}`);
        }
    }
}