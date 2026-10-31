import type {
  PortalData,
  FigureItem,
  FrItem,
  UseCaseInfo,
} from '../types/portal';

// 1. Thông tin chung dự án, 4 Reports, 9 Domains, 6 Canonical Actors
import projectJson from './project.json';

// 2. Các file JSON chứa danh sách Figures chia theo từng Report (dễ chỉnh sửa)
import report1Figures from './figures/report1.json';
import report2Figures from './figures/report2.json';
import report3OverviewFigures from './figures/report3-overview.json';
import report3ScreenFigures from './figures/report3-screens.json';
import report4ClassFigures from './figures/report4-class.json';
import report4SequenceFigures from './figures/report4-sequence.json';

// 3. Các file JSON chứa 141 Functional Requirements chia theo 9 phân hệ (3.2 -> 3.10)
import frsDomain32 from './frs/domain-3.2.json';
import frsDomain33 from './frs/domain-3.3.json';
import frsDomain34 from './frs/domain-3.4.json';
import frsDomain35 from './frs/domain-3.5.json';
import frsDomain36 from './frs/domain-3.6.json';
import frsDomain37 from './frs/domain-3.7.json';
import frsDomain38 from './frs/domain-3.8.json';
import frsDomain39 from './frs/domain-3.9.json';
import frsDomain310 from './frs/domain-3.10.json';

// 4. Các file JSON chứa Use Cases, Business Rules, Messages, Matrices
import useCasesJson from './useCases.json';
import rulesAndMessagesJson from './rulesAndMessages.json';
import matricesJson from './matrices.json';

export const allFigures: FigureItem[] = [
  ...(report1Figures as unknown as FigureItem[]),
  ...(report2Figures as unknown as FigureItem[]),
  ...(report3OverviewFigures as unknown as FigureItem[]),
  ...(report3ScreenFigures as unknown as FigureItem[]),
  ...(report4ClassFigures as unknown as FigureItem[]),
  ...(report4SequenceFigures as unknown as FigureItem[]),
];

export const allFrs: FrItem[] = [
  ...(frsDomain32 as unknown as FrItem[]),
  ...(frsDomain33 as unknown as FrItem[]),
  ...(frsDomain34 as unknown as FrItem[]),
  ...(frsDomain35 as unknown as FrItem[]),
  ...(frsDomain36 as unknown as FrItem[]),
  ...(frsDomain37 as unknown as FrItem[]),
  ...(frsDomain38 as unknown as FrItem[]),
  ...(frsDomain39 as unknown as FrItem[]),
  ...(frsDomain310 as unknown as FrItem[]),
];

export const portalData: PortalData = {
  projectInfo: projectJson.projectInfo as PortalData['projectInfo'],
  reports: projectJson.reports as PortalData['reports'],
  domains: projectJson.domains as PortalData['domains'],
  actors: projectJson.actors as PortalData['actors'],
  useCases: useCasesJson as unknown as UseCaseInfo[],
  screenDescriptions: matricesJson.screenDescriptions,
  screenAuthorization: matricesJson.screenAuthorization,
  nonScreenFunctions: matricesJson.nonScreenFunctions,
  entities: matricesJson.entities,
  businessRules: rulesAndMessagesJson.businessRules,
  messages: rulesAndMessagesJson.messages,
  frs: allFrs,
  figures: allFigures,
};

export default portalData;

