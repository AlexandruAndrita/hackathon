/**
 * works only for the following legal forms:
 * - GmbH      ("gmbh")
 * - KG        ("kg")
 * - e.K.      ("ek")
 * - eGbR      ("egbr")
 * - OHG       ("ohg")
 */

import Openregister from 'openregister';
import 'dotenv/config';
import fs from 'fs';

const client = new Openregister({
apiKey: process.env.OPEN_REGISTER_API_KEY,
});

const company_ids = ['DE-HRB-M1201-128843', 'DE-HRB-M1201-43507'];

for (const company_id of company_ids) {
    const response = await client.company.getOwnersV1(company_id);

    const output = JSON.stringify(response, null, 2);

    const title = "openregister_get_company_owners";
    const filename = `${title}_${company_id}.txt`;

    // write to file
    fs.writeFileSync(filename, output);

    //console.log(response.company_id);
}

