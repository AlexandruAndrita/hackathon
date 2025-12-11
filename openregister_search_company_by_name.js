import Openregister from 'openregister';
import 'dotenv/config';

const client = new Openregister({
    apiKey: process.env.OPEN_REGISTER_API_KEY,
});

const response = await client.search.autocompleteCompaniesV1({ query: 'ODDO BHF SE' });

console.log(response.results);