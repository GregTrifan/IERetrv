# IEF Project summariser

This project is used for automating the creation of wikis for the [IEF](https://impactevaluation.foundation/)

Steps to run this codebase:

1. `pip install -r requirements.txt`
2. `python c_copy_export.py ` - Scrape https://carboncopy.news/projects and get all the projects featured there in `resources/carboncopy_projects.csv`
3. `python export_unique.csv` - generates `resources/mixed_data.csv`, which will hold all projects that are featured in https://carboncopy.news/projects and https://positiveblockchain.io/
4. `python info_export.py` - Scrape all the projects featured in `resources/mixed_data.csv` and generate relevant information in `info/PROJECT_NAME.txt`
5. `python gen_summary.py` - Uses ChatGPT to generate project summaries using the info from `info/PROJECT_NAME.txt`, the summary being stored in ``sumaries/PROJECT_NAME.txt`
6. _(Coming soon)_ `python get_wikis.py` - generates wiki pages for https://impact.miraheze.org/ and archives project websites on WebArchive

In order to run this, you'll need to get also get the projects list from https://positiveblockchain.io/ and save it as `resources/PositiveBlockchain_data.csv`

Summary example - https://www.carbon-counting-club.com/

> The Carbon Counting Club is an innovative online gardening initiative focused on environmental sustainability. Its mission is to raise funds for tree planting while rewarding individuals who engage in at-home carbon sequestration methods. Participants can buy NFTs that contribute to tree planting and support public goods, and they can earn cryptocurrency rewards for sharing their gardening efforts on social media. The project encourages community involvement through a bounty board and offers guidelines for effective carbon capture materials.
> The project employs unique technologies such as NFTs to facilitate funding and rewards, fostering a participatory approach to environmental conservation. Partnerships are likely established within the crypto and gardening communities, enabling members to claim Carbon Counting Coins by promoting their gardening activities on platforms like X, thus integrating social media engagement with eco-friendly practices.
