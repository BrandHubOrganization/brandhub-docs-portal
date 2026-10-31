export type CanonicalRole = 'Guest' | 'Owner' | 'Manager' | 'Creator' | 'Client' | 'Admin';

export interface ProjectInfo {
  name: string;
  course: string;
  cloudinaryCloudName: string;
  totalFrs: number;
  totalUseCases: number;
  totalBusinessRules: number;
  totalMessages: number;
  totalFigures: number;
  canonicalRoles: CanonicalRole[];
  supportedPlatforms: string[];
  paymentGateway: string;
}

export interface ReportInfo {
  id: string;
  code: string;
  title: string;
  fileName: string;
  description: string;
  figureCount: number;
}

export interface DomainInfo {
  code: string;
  title: string;
  frCount: number;
  summary: string;
}

export interface ActorInfo {
  index: string;
  role: string;
  description: string;
}

export interface UseCaseInfo {
  id: string;
  name: string;
  actors: CanonicalRole[];
  actorsRaw: string;
  description: string;
  ucNum: number;
  frCode?: string;
}

export interface ScreenDescription {
  index: string;
  feature: string;
  screen: string;
  description: string;
}

export interface ScreenAuthRow {
  screen: string;
  Admin: string;
  Owner: string;
  Manager: string;
  Creator: string;
  Client: string;
  Guest: string;
}

export interface NonScreenFunc {
  index: string;
  feature: string;
  systemFunction: string;
  description: string;
}

export interface EntityInfo {
  index: string;
  entity: string;
  description: string;
}

export interface BusinessRuleItem {
  code: string;
  definition: string;
  relatedFrs: string[];
}

export interface MessageItem {
  index: string;
  code: string;
  type: string;
  context: string;
  content: string;
  relatedFrs: string[];
}

export interface DataSpecs {
  inputRequired: string;
  inputOptional: string;
  systemData: string;
  output: string;
}

export interface FrBrInline {
  code: string;
  text: string;
}

export interface FrItem {
  code: string;
  title: string;
  domainCode: string;
  domainTitle: string;
  ucId: string;
  ucName: string;
  ucDescription: string;
  figureId: string;
  figureNumber: number;
  figureCaption: string;
  sequenceFigureId: string;
  classDiagramFigureId: string;
  actors: CanonicalRole[];
  trigger: string;
  purpose: string;
  viSummary: string;
  docAuthor: string;
  codeAuthor: string;
  interface: string;
  dataProcessing: string;
  dataSpecs: DataSpecs;
  businessRules: FrBrInline[];
  linkedBrCodes: string[];
  linkedMsgCodes: string[];
  validations: string[];
  normalFlow: string[];
  abnormalCases: string[];
  postConditions: string[];
  screenImageUrl: string;
  sequenceImageUrl: string;
  classDiagramImageUrl: string;
}

export interface FigureComponent {
  name: string;
  type: string;
  description: string;
}

export interface SequenceLifeline {
  name: string;
  stereotype: string;
  description: string;
}

export interface SequenceMessage {
  step: number;
  from: string;
  to: string;
  fromIdx: number;
  toIdx: number;
  isReturn: boolean;
  label: string;
}

export interface SubImageItem {
  id: string;
  label: string;
  imageUrl: string;
  width: number;
  height: number;
}

export interface FigureItem {
  figNum: number;
  id: string;
  title: string;
  caption: string;
  section: string;
  domainCode?: string;
  domainTitle?: string;
  frCode?: string;
  ucId?: string;
  category: string;
  imageSourceType?: string;
  actors: CanonicalRole[];
  summary: string;
  viSummary?: string;
  interface?: string;
  dataProcessing?: string;
  trigger?: string;
  dataSpecs?: DataSpecs;
  businessRules?: FrBrInline[];
  linkedBrCodes?: string[];
  linkedMsgCodes?: string[];
  validations?: string[];
  normalFlow?: string[];
  abnormalCases?: string[];
  postConditions?: string[];
  sequenceFigureId?: string;
  screenFigureId?: string;
  classDiagramFigureId?: string;
  lifelines?: SequenceLifeline[];
  sequenceMessages?: SequenceMessage[];
  reportId: string;
  reportName: string;
  components: FigureComponent[];
  imageUrl: string;
  imageWidth: number;
  imageHeight: number;
  imageBytes: number;
  subImages?: SubImageItem[];
}

export interface PortalData {
  projectInfo: ProjectInfo;
  reports: ReportInfo[];
  domains: DomainInfo[];
  actors: ActorInfo[];
  useCases: UseCaseInfo[];
  screenDescriptions: ScreenDescription[];
  screenAuthorization: ScreenAuthRow[];
  nonScreenFunctions: NonScreenFunc[];
  entities: EntityInfo[];
  businessRules: BusinessRuleItem[];
  messages: MessageItem[];
  frs: FrItem[];
  figures: FigureItem[];
}

