# Chaîne de conversions

## Graphe

La logique derrière ce projet est la suivante :

1. Prendre un fichier IDML en entrée, et le donner à [`idml2xml-frontend`](https://github.com/transpect/idml2xml-frontend) pour obtenir un fichier [Hub XML](https://github.com/le-tex/Hub) ;
2. À partir de ce fichier, le "nettoyer" pour obtenir un document dans la spécification DocBook 5.1, supportée par Pandoc ;

Ces deux premières étapes sont les objectifs du paquet `idml2docbook` développé pour ce projet.

3. Lire le fichier DocBook produit avec la [version modifiée de Pandoc](https://github.com/yanntrividic/pandoc/) ;
4. Appliquer des filtres Lua pour correctement structurer l'[arbre de syntaxe abstraite](https://fr.wikipedia.org/wiki/Arbre_de_la_syntaxe_abstraite) (AST) de Pandoc ;
5. Utiliser le _writer_ de Pandoc souhaité.

```{graphviz} ../graphs/conversions.dot
:caption: _Graphe des conversions à l'œuvre dans ce projet._
:align: center
```

## Détail des conversions

Cette section retrace la série d'opérations effectuées sur le fichier `hello_world.idml` pour arriver jusqu'à sa version en Markdown. Cela commence donc avec le fichier IDML (34 Ko pour un "Hello world!"), qui consiste en un ensemble de fichiers XML dont voici l'arborescence :

```
hello_world.idml
├── designmap.xml
├── MasterSpreads
│   └── MasterSpread_ud5.xml
├── META-INF
│   ├── container.xml
│   └── metadata.xml
├── mimetype
├── Resources
│   ├── Fonts.xml
│   ├── Graphic.xml
│   ├── Preferences.xml
│   └── Styles.xml
├── Spreads
│   └── Spread_uce.xml
├── Stories
│   └── Story_ue7.xml
└── XML
    ├── BackingStory.xml
    └── Tags.xml
```

Les informations nous intéressant sont d'abord contenues dans le fichier `designmap.xml` :

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<?aid style="50" type="document" readerVersion="6.0" featureSet="257" product="16.4(54)" ?>
<Document xmlns:idPkg="http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging" DOMVersion="16.2" Self="d" StoryList="ue7 ub0" Name="Sans titre-1" ZeroPoint="0 0" ActiveLayer="ucb" CMYKProfile="Coated FOGRA39 (ISO 12647-2:2004)" RGBProfile="sRGB IEC61966-2.1" SolidColorIntent="UseColorSettings" AfterBlendingIntent="UseColorSettings" DefaultImageIntent="UseColorSettings" RGBPolicy="PreserveEmbeddedProfiles" CMYKPolicy="CombinationOfPreserveAndSafeCmyk" AccurateLABSpots="false">
        <Properties>
                <Label>
                        <KeyValuePair Key="kAdobeDPS_Version" Value="2" />
                </Label>
        </Properties>
        <Language Self="Language/$ID/[No Language]" Name="$ID/[No Language]" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/[No Language]" SublanguageName="$ID/[No Language]" Id="0" HyphenationVendor="$ID/" SpellingVendor="$ID/" />
        <Language Self="Language/$ID/German%3a Reformed" Name="$ID/German: Reformed" SingleQuotes="‚‘" DoubleQuotes="„“" PrimaryLanguageName="$ID/German" SublanguageName="$ID/Reformed" Id="275" HyphenationVendor="Duden" SpellingVendor="Duden" />
        <Language Self="Language/$ID/de_DE_2006" Name="$ID/de_DE_2006" SingleQuotes="‚‘" DoubleQuotes="„“" PrimaryLanguageName="$ID/de_DE_2006" SublanguageName="$ID/" Id="275" HyphenationVendor="Duden" SpellingVendor="Duden" />
        <Language Self="Language/$ID/German%3a Swiss" Name="$ID/German: Swiss" SingleQuotes="‹›" DoubleQuotes="«»" PrimaryLanguageName="$ID/German" SublanguageName="$ID/Swiss" Id="531" HyphenationVendor="Duden" SpellingVendor="Duden" />
        <Language Self="Language/$ID/de_CH_2006" Name="$ID/de_CH_2006" SingleQuotes="‹›" DoubleQuotes="«»" PrimaryLanguageName="$ID/de_CH_2006" SublanguageName="$ID/" Id="531" HyphenationVendor="Duden" SpellingVendor="Duden" />
        <Language Self="Language/$ID/German%3a Austrian" Name="$ID/German: Austrian" SingleQuotes="‚‘" DoubleQuotes="„“" PrimaryLanguageName="$ID/German" SublanguageName="$ID/Austrian" Id="787" HyphenationVendor="Duden" SpellingVendor="Duden" />
        <Language Self="Language/$ID/bn_IN" Name="$ID/bn_IN" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/gu_IN" Name="$ID/gu_IN" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/hi_IN" Name="$ID/hi_IN" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/kn_IN" Name="$ID/kn_IN" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/ml_IN" Name="$ID/ml_IN" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/mr_IN" Name="$ID/mr_IN" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/or_IN" Name="$ID/or_IN" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/pa_IN" Name="$ID/pa_IN" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/ta_IN" Name="$ID/ta_IN" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/te_IN" Name="$ID/te_IN" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Bulgarian" Name="$ID/Bulgarian" SingleQuotes="‚‘" DoubleQuotes="„“" PrimaryLanguageName="$ID/Bulgarian" SublanguageName="$ID/" Id="261" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Catalan" Name="$ID/Catalan" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/Catalan" SublanguageName="$ID/" Id="263" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Czech" Name="$ID/Czech" SingleQuotes="‚‘" DoubleQuotes="„“" PrimaryLanguageName="$ID/Czech" SublanguageName="$ID/" Id="266" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Danish" Name="$ID/Danish" SingleQuotes="’’" DoubleQuotes="””" PrimaryLanguageName="$ID/Danish" SublanguageName="$ID/" Id="267" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Greek" Name="$ID/Greek" SingleQuotes="‘’" DoubleQuotes="«»" PrimaryLanguageName="$ID/Greek" SublanguageName="$ID/" Id="276" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/English%3a Canadian" Name="$ID/English: Canadian" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/English" SublanguageName="$ID/Canadian" Id="1037" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/English%3a UK" Name="$ID/English: UK" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/English" SublanguageName="$ID/UK" Id="525" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/English%3a USA" Name="$ID/English: USA" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/English" SublanguageName="$ID/USA" Id="269" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/English%3a USA Medical" Name="$ID/English: USA Medical" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/English" SublanguageName="$ID/USA Medical" Id="269" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Spanish%3a Castilian" Name="$ID/Spanish: Castilian" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/Spanish" SublanguageName="$ID/Castilian" Id="294" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Estonian" Name="$ID/Estonian" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/Estonian" SublanguageName="$ID/" Id="270" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Finnish" Name="$ID/Finnish" SingleQuotes="’’" DoubleQuotes="””" PrimaryLanguageName="$ID/Finnish" SublanguageName="$ID/" Id="273" HyphenationVendor="Hunspell" SpellingVendor="Proximity" />
        <Language Self="Language/$ID/French%3a Canadian" Name="$ID/French: Canadian" SingleQuotes="‘’" DoubleQuotes="«»" PrimaryLanguageName="$ID/French" SublanguageName="$ID/Canadian" Id="786" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/French" Name="$ID/French" SingleQuotes="‘’" DoubleQuotes="«»" PrimaryLanguageName="$ID/French" SublanguageName="$ID/" Id="274" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Croatian" Name="$ID/Croatian" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/Croatian" SublanguageName="$ID/" Id="265" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Hungarian" Name="$ID/Hungarian" SingleQuotes="‚’" DoubleQuotes="„”" PrimaryLanguageName="$ID/Hungarian" SublanguageName="$ID/" Id="278" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Italian" Name="$ID/Italian" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/Italian" SublanguageName="$ID/" Id="281" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Lithuanian" Name="$ID/Lithuanian" SingleQuotes="‚‘" DoubleQuotes="„“" PrimaryLanguageName="$ID/Lithuanian" SublanguageName="$ID/" Id="285" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Latvian" Name="$ID/Latvian" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/Latvian" SublanguageName="$ID/" Id="284" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Norwegian%3a Bokmal" Name="$ID/Norwegian: Bokmal" SingleQuotes="’’" DoubleQuotes="””" PrimaryLanguageName="$ID/Norwegian" SublanguageName="$ID/Bokmal" Id="286" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Dutch" Name="$ID/Dutch" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/Dutch" SublanguageName="$ID/" Id="268" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/nl_NL_2005" Name="$ID/nl_NL_2005" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/nl_NL_2005" SublanguageName="$ID/" Id="268" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Norwegian%3a Nynorsk" Name="$ID/Norwegian: Nynorsk" SingleQuotes="’’" DoubleQuotes="””" PrimaryLanguageName="$ID/Norwegian" SublanguageName="$ID/Nynorsk" Id="542" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Polish" Name="$ID/Polish" SingleQuotes="‚’" DoubleQuotes="„”" PrimaryLanguageName="$ID/Polish" SublanguageName="$ID/" Id="287" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Portuguese%3a Brazilian" Name="$ID/Portuguese: Brazilian" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/Portuguese" SublanguageName="$ID/Brazilian" Id="544" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Portuguese%3a Orthographic Agreement" Name="$ID/Portuguese: Orthographic Agreement" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/Portuguese" SublanguageName="$ID/Orthographic Agreement" Id="544" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Portuguese" Name="$ID/Portuguese" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/Portuguese" SublanguageName="$ID/" Id="288" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Romanian" Name="$ID/Romanian" SingleQuotes="‚’" DoubleQuotes="„”" PrimaryLanguageName="$ID/Romanian" SublanguageName="$ID/" Id="289" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Russian" Name="$ID/Russian" SingleQuotes="‘’" DoubleQuotes="«»" PrimaryLanguageName="$ID/Russian" SublanguageName="$ID/" Id="290" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Slovak" Name="$ID/Slovak" SingleQuotes="‚‘" DoubleQuotes="„“" PrimaryLanguageName="$ID/Slovak" SublanguageName="$ID/" Id="291" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Slovenian" Name="$ID/Slovenian" SingleQuotes="&apos;&apos;" DoubleQuotes="»«" PrimaryLanguageName="$ID/Slovenian" SublanguageName="$ID/" Id="292" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Swedish" Name="$ID/Swedish" SingleQuotes="’’" DoubleQuotes="””" PrimaryLanguageName="$ID/Swedish" SublanguageName="$ID/" Id="295" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Turkish" Name="$ID/Turkish" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/Turkish" SublanguageName="$ID/" Id="297" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Ukrainian" Name="$ID/Ukrainian" SingleQuotes="‘’" DoubleQuotes="«»" PrimaryLanguageName="$ID/Ukrainian" SublanguageName="$ID/" Id="298" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/id_ID" Name="$ID/id_ID" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/km_KH" Name="$ID/km_KH" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/lo_LA" Name="$ID/lo_LA" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/my_MM" Name="$ID/my_MM" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/si_LK" Name="$ID/si_LK" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/" SublanguageName="$ID/" Id="348" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Thai" Name="$ID/Thai" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/Thai" SublanguageName="$ID/" Id="296" HyphenationVendor="Hunspell" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/English%3a USA Legal" Name="$ID/English: USA Legal" SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/English" SublanguageName="$ID/USA Legal" Id="269" HyphenationVendor="Proximity" SpellingVendor="Proximity" />
        <Language Self="Language/$ID/German%3a Traditional" Name="$ID/German: Traditional" SingleQuotes="‚‘" DoubleQuotes="„“" PrimaryLanguageName="$ID/German" SublanguageName="$ID/Traditional" Id="275" HyphenationVendor="Proximity" SpellingVendor="Proximity" />
        <Language Self="Language/$ID/Hebrew" Name="$ID/Hebrew" SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" PrimaryLanguageName="$ID/Hebrew" SublanguageName="$ID/" Id="277" HyphenationVendor="WinSoft" SpellingVendor="Hunspell" />
        <Language Self="Language/$ID/Arabic" Name="$ID/Arabic" SingleQuotes="‹›" DoubleQuotes="«»" PrimaryLanguageName="$ID/Arabic" SublanguageName="$ID/" Id="257" HyphenationVendor="$ID/" SpellingVendor="Hunspell" />
        <idPkg:Graphic src="Resources/Graphic.xml" />
        <idPkg:Fonts src="Resources/Fonts.xml" />
        <idPkg:Styles src="Resources/Styles.xml" />
        <NumberingList Self="NumberingList/$ID/[Default]" Name="$ID/[Default]" ContinueNumbersAcrossStories="false" ContinueNumbersAcrossDocuments="false" />
        <NamedGrid Self="NamedGrid/$ID/[Page Grid]" Name="$ID/[Page Grid]">
                <GridDataInformation FontStyle="Regular" PointSize="12" CharacterAki="0" LineAki="9" HorizontalScale="100" VerticalScale="100" LineAlignment="LeftOrTopLineJustify" GridAlignment="AlignEmCenter" CharacterAlignment="AlignEmCenter">
                        <Properties>
                                <AppliedFont type="string">Minion Pro</AppliedFont>
                        </Properties>
                </GridDataInformation>
        </NamedGrid>
        <ConditionalTextPreference ShowConditionIndicators="ShowIndicators" ActiveConditionSet="n" />
        <idPkg:Preferences src="Resources/Preferences.xml" />
        <EndnoteOption EndnoteTitle="Notes de fin" EndnoteTitleStyle="ParagraphStyle/$ID/NormalParagraphStyle" StartEndnoteNumberAt="1" EndnoteMarkerStyle="CharacterStyle/$ID/[No character style]" EndnoteTextStyle="ParagraphStyle/$ID/NormalParagraphStyle" EndnoteSeparatorText="&#x9;" EndnotePrefix="" EndnoteSuffix="">
                <Properties>
                        <EndnoteNumberingStyle type="enumeration">Arabic</EndnoteNumberingStyle>
                        <RestartEndnoteNumbering type="enumeration">Continuous</RestartEndnoteNumbering>
                        <EndnoteMarkerPositioning type="enumeration">SuperscriptMarker</EndnoteMarkerPositioning>
                        <ScopeValue type="enumeration">EndnoteDocumentScope</ScopeValue>
                        <FrameCreateOption type="enumeration">NewPage</FrameCreateOption>
                        <ShowEndnotePrefixSuffix type="enumeration">NoPrefixSuffix</ShowEndnotePrefixSuffix>
                </Properties>
        </EndnoteOption>
        <TextFrameFootnoteOptionsObject EnableOverrides="false" SpanFootnotesAcross="false" MinimumSpacingOption="12" SpaceBetweenFootnotes="6" />
        <LinkedStoryOption UpdateWhileSaving="false" WarnOnUpdateOfEditedStory="true" RemoveForcedLineBreaks="false" ApplyStyleMappings="false" />
        <LinkedPageItemOption UpdateLinkWhileSaving="false" WarnOnUpdateOfEditedPageItem="true" PreserveSizeAndShape="false" PreserveAppearance="false" PreserveInteractivity="false" PreserveFrameContent="false" PreserveOthers="false" />
        <WatermarkPreference WatermarkVisibility="false" WatermarkDoPrint="false" WatermarkDrawInBack="true" WatermarkText="" WatermarkFontFamily="Minion Pro" WatermarkFontStyle="Regular" WatermarkFontPointSize="48" WatermarkOpacity="50" WatermarkRotation="0" WatermarkHorizontalPosition="WatermarkHCenter" WatermarkHorizontalOffset="0" WatermarkVerticalPosition="WatermarkVCenter" WatermarkVerticalOffset="0">
                <Properties>
                        <WatermarkFontColor type="enumeration">Black</WatermarkFontColor>
                </Properties>
        </WatermarkPreference>
        <TaggedPDFPreference StructureOrder="UseXMLStructure" />
        <AdjustLayoutPreference EnableAdjustLayout="false" AllowLockedObjectsToAdjust="true" AllowFontSizeAndLeadingAdjustment="false" ImposeFontSizeRestriction="false" MinimumFontSize="6" MaximumFontSize="324" EnableAutoAdjustMargins="false" />
        <HTMLFXLExportPreference EpubPageRange="" EpubPageRangeFormat="ExportAllPages" />
        <PublishExportPreference PublishCover="FirstPage" CoverImageFile="" PublishPageRange="" PublishPageRangeFormat="ExportAllPages" ImageConversion="Automatic" ImageExportResolution="Ppi96" PublishDescription="" PublishFileName="" PublishFormat="PublishByPages" CoverPage="$ID/" GIFOptionsPalette="AdaptivePalette" JPEGOptionsQuality="High" PublishPdf="false" />
        <TextVariable Self="dTextVariablen&lt;?AID 001b?&gt;TV XRefChapterNumber" Name="&lt;?AID 001b?&gt;TV XRefChapterNumber" VariableType="XrefChapterNumberType" />
        <TextVariable Self="dTextVariablen&lt;?AID 001b?&gt;TV XRefPageNumber" Name="&lt;?AID 001b?&gt;TV XRefPageNumber" VariableType="XrefPageNumberType" />
        <TextVariable Self="dTextVariablenDate de création" Name="Date de création" VariableType="CreationDateType">
                <DateVariablePreference TextBefore="" Format="dd/MM/yy" TextAfter="" />
        </TextVariable>
        <TextVariable Self="dTextVariablenDate de modification" Name="Date de modification" VariableType="ModificationDateType">
                <DateVariablePreference TextBefore="" Format="d MMMM yyyy h:mm" TextAfter="" />
        </TextVariable>
        <TextVariable Self="dTextVariablenDate de sortie" Name="Date de sortie" VariableType="OutputDateType">
                <DateVariablePreference TextBefore="" Format="dd/MM/yy" TextAfter="" />
        </TextVariable>
        <TextVariable Self="dTextVariablenDernier numéro de page" Name="Dernier numéro de page" VariableType="LastPageNumberType">
                <PageNumberVariablePreference TextBefore="" Format="Current" TextAfter="" Scope="SectionScope" />
        </TextVariable>
        <TextVariable Self="dTextVariablenEn-tête continu" Name="En-tête continu" VariableType="MatchParagraphStyleType">
                <MatchParagraphStylePreference TextBefore="" TextAfter="" AppliedParagraphStyle="ParagraphStyle/$ID/NormalParagraphStyle" SearchStrategy="FirstOnPage" ChangeCase="None" DeleteEndPunctuation="false" />
        </TextVariable>
        <TextVariable Self="dTextVariablenNom de fichier" Name="Nom de fichier" VariableType="FileNameType">
                <FileNameVariablePreference TextBefore="" IncludePath="false" IncludeExtension="false" TextAfter="" />
        </TextVariable>
        <TextVariable Self="dTextVariablenNom de l&apos;image" Name="Nom de l&apos;image" VariableType="LiveCaptionType">
                <CaptionMetadataVariablePreference TextBefore="" MetadataProviderName="$ID/#LinkInfoNameStr" TextAfter="" />
        </TextVariable>
        <TextVariable Self="dTextVariablenNuméro de chapitre" Name="Numéro de chapitre" VariableType="ChapterNumberType">
                <ChapterNumberVariablePreference TextBefore="" Format="Current" TextAfter="" />
        </TextVariable>
        <idPkg:Tags src="XML/Tags.xml" />
        <Layer Self="ucb" Name="Calque 1" Visible="true" Locked="false" IgnoreWrap="false" ShowGuides="true" LockGuides="false" UI="true" Expendable="true" Printable="true">
                <Properties>
                        <LayerColor type="enumeration">LightBlue</LayerColor>
                </Properties>
        </Layer>
        <idPkg:MasterSpread src="MasterSpreads/MasterSpread_ud5.xml" />
        <idPkg:Spread src="Spreads/Spread_uce.xml" />
        <Section Self="ud4" Length="1" Name="" ContinueNumbering="true" IncludeSectionPrefix="false" Marker="" PageStart="ud3" SectionPrefix="" AlternateLayoutLength="1" AlternateLayout="A4 V">
                <Properties>
                        <PageNumberStyle type="enumeration">Arabic</PageNumberStyle>
                </Properties>
        </Section>
        <DocumentUser Self="dDocumentUser0" UserName="$ID/Unknown User Name">
                <Properties>
                        <UserColor type="enumeration">Gold</UserColor>
                </Properties>
        </DocumentUser>
        <CrossReferenceFormat Self="u9e" Name="Paragraphe entier et numéro de page" AppliedCharacterStyle="n">
                <BuildingBlock Self="u9eBuildingBlock0" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="&quot;" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="u9eBuildingBlock1" BlockType="FullParagraphBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="u9eBuildingBlock2" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="&quot;, page " AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="u9eBuildingBlock3" BlockType="PageNumberBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
        </CrossReferenceFormat>
        <CrossReferenceFormat Self="u9f" Name="Paragraphe entier" AppliedCharacterStyle="n">
                <BuildingBlock Self="u9fBuildingBlock0" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="&quot;" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="u9fBuildingBlock1" BlockType="FullParagraphBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="u9fBuildingBlock2" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="&quot;" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
        </CrossReferenceFormat>
        <CrossReferenceFormat Self="ua0" Name="Texte du paragraphe et numéro de page" AppliedCharacterStyle="n">
                <BuildingBlock Self="ua0BuildingBlock0" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="&quot;" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua0BuildingBlock1" BlockType="ParagraphTextBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua0BuildingBlock2" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="&quot;, page " AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua0BuildingBlock3" BlockType="PageNumberBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
        </CrossReferenceFormat>
        <CrossReferenceFormat Self="ua1" Name="Texte du paragraphe" AppliedCharacterStyle="n">
                <BuildingBlock Self="ua1BuildingBlock0" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="&quot;" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua1BuildingBlock1" BlockType="ParagraphTextBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua1BuildingBlock2" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="&quot;" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
        </CrossReferenceFormat>
        <CrossReferenceFormat Self="ua2" Name="Numéro de paragraphe et numéro de page" AppliedCharacterStyle="n">
                <BuildingBlock Self="ua2BuildingBlock0" BlockType="ParagraphNumberBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua2BuildingBlock1" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText=", page " AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua2BuildingBlock2" BlockType="PageNumberBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
        </CrossReferenceFormat>
        <CrossReferenceFormat Self="ua3" Name="Numéro de paragraphe" AppliedCharacterStyle="n">
                <BuildingBlock Self="ua3BuildingBlock0" BlockType="ParagraphNumberBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
        </CrossReferenceFormat>
        <CrossReferenceFormat Self="ua4" Name="Nom de l&apos;ancre de texte &amp; numéro de page" AppliedCharacterStyle="n">
                <BuildingBlock Self="ua4BuildingBlock0" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="&quot;" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua4BuildingBlock1" BlockType="BookmarkNameBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua4BuildingBlock2" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="&quot;, page " AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua4BuildingBlock3" BlockType="PageNumberBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
        </CrossReferenceFormat>
        <CrossReferenceFormat Self="ua5" Name="Nom de l&apos;ancre de texte" AppliedCharacterStyle="n">
                <BuildingBlock Self="ua5BuildingBlock0" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="&quot;" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua5BuildingBlock1" BlockType="BookmarkNameBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua5BuildingBlock2" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="&quot;" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
        </CrossReferenceFormat>
        <CrossReferenceFormat Self="ua6" Name="Numéro de page" AppliedCharacterStyle="n">
                <BuildingBlock Self="ua6BuildingBlock0" BlockType="CustomStringBuildingBlock" AppliedCharacterStyle="n" CustomText="page " AppliedDelimiter="$ID/" IncludeDelimiter="false" />
                <BuildingBlock Self="ua6BuildingBlock1" BlockType="PageNumberBuildingBlock" AppliedCharacterStyle="n" CustomText="$ID/" AppliedDelimiter="$ID/" IncludeDelimiter="false" />
        </CrossReferenceFormat>
        <idPkg:BackingStory src="XML/BackingStory.xml" />
        <idPkg:Story src="Stories/Story_ue7.xml" />
        <ColorGroup Self="ColorGroup/[Root Color Group]" Name="[Root Color Group]" IsRootColorGroup="true">
                <ColorGroupSwatch Self="u18ColorGroupSwatch0" SwatchItemRef="Swatch/None" />
                <ColorGroupSwatch Self="u18ColorGroupSwatch1" SwatchItemRef="Color/Registration" />
                <ColorGroupSwatch Self="u18ColorGroupSwatch2" SwatchItemRef="Color/Paper" />
                <ColorGroupSwatch Self="u18ColorGroupSwatch3" SwatchItemRef="Color/Black" />
                <ColorGroupSwatch Self="u18ColorGroupSwatch4" SwatchItemRef="Color/C=100 M=0 J=0 N=0" />
                <ColorGroupSwatch Self="u18ColorGroupSwatch5" SwatchItemRef="Color/C=0 M=100 J=0 N=0" />
                <ColorGroupSwatch Self="u18ColorGroupSwatch6" SwatchItemRef="Color/C=0 M=0 J=100 N=0" />
                <ColorGroupSwatch Self="u18ColorGroupSwatch7" SwatchItemRef="Color/C=15 M=100 J=100 N=0" />
                <ColorGroupSwatch Self="u18ColorGroupSwatch8" SwatchItemRef="Color/C=75 M=5 J=100 N=0" />
                <ColorGroupSwatch Self="u18ColorGroupSwatch9" SwatchItemRef="Color/C=100 M=90 J=10 N=0" />
        </ColorGroup>
        <IndexingSortOption Self="dIndexingSortOptionnkIndexGroup_Symbol" Name="$ID/kIndexGroup_Symbol" Include="true" Priority="0" HeaderType="Nothing" />
        <IndexingSortOption Self="dIndexingSortOptionnkIndexGroup_Alphabet" Name="$ID/kIndexGroup_Alphabet" Include="true" Priority="1" HeaderType="BasicLatin" />
        <IndexingSortOption Self="dIndexingSortOptionnkIndexGroup_Numeric" Name="$ID/kIndexGroup_Numeric" Include="false" Priority="2" HeaderType="Nothing" />
        <IndexingSortOption Self="dIndexingSortOptionnkWRIndexGroup_GreekAlphabet" Name="$ID/kWRIndexGroup_GreekAlphabet" Include="false" Priority="3" HeaderType="Nothing" />
        <IndexingSortOption Self="dIndexingSortOptionnkWRIndexGroup_CyrillicAlphabet" Name="$ID/kWRIndexGroup_CyrillicAlphabet" Include="false" Priority="4" HeaderType="Russian" />
        <IndexingSortOption Self="dIndexingSortOptionnkIndexGroup_Kana" Name="$ID/kIndexGroup_Kana" Include="false" Priority="5" HeaderType="HiraganaAll" />
        <IndexingSortOption Self="dIndexingSortOptionnkIndexGroup_Chinese" Name="$ID/kIndexGroup_Chinese" Include="false" Priority="6" HeaderType="ChinesePinyin" />
        <IndexingSortOption Self="dIndexingSortOptionnkIndexGroup_Korean" Name="$ID/kIndexGroup_Korean" Include="false" Priority="7" HeaderType="KoreanConsonant" />
        <IndexingSortOption Self="dIndexingSortOptionnkWRIndexGroup_ArabicAlphabet" Name="$ID/kWRIndexGroup_ArabicAlphabet" Include="false" Priority="8" HeaderType="Nothing" />
        <IndexingSortOption Self="dIndexingSortOptionnkWRIndexGroup_HebrewAlphabet" Name="$ID/kWRIndexGroup_HebrewAlphabet" Include="false" Priority="9" HeaderType="Nothing" />
        <ABullet Self="dABullet0" CharacterType="UnicodeOnly" CharacterValue="8226">
                <Properties>
                        <BulletsFont type="string">$ID/</BulletsFont>
                        <BulletsFontStyle type="string">$ID/</BulletsFontStyle>
                </Properties>
        </ABullet>
        <ABullet Self="dABullet1" CharacterType="UnicodeOnly" CharacterValue="42">
                <Properties>
                        <BulletsFont type="string">$ID/</BulletsFont>
                        <BulletsFontStyle type="string">$ID/</BulletsFontStyle>
                </Properties>
        </ABullet>
        <ABullet Self="dABullet2" CharacterType="UnicodeOnly" CharacterValue="9674">
                <Properties>
                        <BulletsFont type="string">$ID/</BulletsFont>
                        <BulletsFontStyle type="string">$ID/</BulletsFontStyle>
                </Properties>
        </ABullet>
        <ABullet Self="dABullet3" CharacterType="UnicodeWithFont" CharacterValue="187">
                <Properties>
                        <BulletsFont type="string">Myriad Pro</BulletsFont>
                        <BulletsFontStyle type="string">$ID/Regular</BulletsFontStyle>
                </Properties>
        </ABullet>
        <ABullet Self="dABullet4" CharacterType="GlyphWithFont" CharacterValue="503">
                <Properties>
                        <BulletsFont type="string">Minion Pro</BulletsFont>
                        <BulletsFontStyle type="string">$ID/Regular</BulletsFontStyle>
                </Properties>
        </ABullet>
        <Assignment Self="udc" Name="$ID/UnassignedInCopy" UserName="$ID/" ExportOptions="AssignedSpreads" IncludeLinksWhenPackage="true" FilePath="$ID/">
                <Properties>
                        <FrameColor type="enumeration">Nothing</FrameColor>
                </Properties>
        </Assignment>
</Document>
```

Ce fichier indique l'ordre des _stories_ (blocs chaînés), qui ne peut pas être inféré depuis le dossier `stories` seulement. Dans ce cas, il n'y a qu'un seul bloc, donc une seule _story_,  soit le fichier `Story_ue7.xml`, dans lequel figure bien bien `Hello world!` :

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<idPkg:Story xmlns:idPkg="http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging" DOMVersion="16.2">
        <Story Self="ue7" UserText="true" IsEndnoteStory="false" AppliedTOCStyle="n" TrackChanges="false" StoryTitle="$ID/" AppliedNamedGrid="n">
                <StoryPreference OpticalMarginAlignment="false" OpticalMarginSize="12" FrameType="TextFrameType" StoryOrientation="Horizontal" StoryDirection="LeftToRightDirection" />
                <InCopyExportOption IncludeGraphicProxies="true" IncludeAllResources="false" />
                <ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/$ID/NormalParagraphStyle">
                        <CharacterStyleRange AppliedCharacterStyle="CharacterStyle/$ID/[No character style]">
                                <Properties>
                                        <AppliedFont type="string">Arial</AppliedFont>
                                </Properties>
                                <Content>Hello world!</Content>
                        </CharacterStyleRange>
                </ParagraphStyleRange>
        </Story>
</idPkg:Story>
```

C'est principalement ces informations qui seront retenues par `idml2xml-frontend`. Le fichier obtenu est déjà bien moins lourd, et contient les informations suivantes :


```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="http://www.le-tex.de/resource/schema/hub/1.2/hub.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-model href="http://www.le-tex.de/resource/schema/hub/1.2/hub.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>
<hub xmlns="http://docbook.org/ns/docbook"
     xmlns:css="http://www.w3.org/1996/css"
     xml:lang="fr-FR"
     version="5.1-variant le-tex_Hub-1.2"
     css:version="3.0-variant le-tex_Hub-1.2"
     css:rule-selection-attribute="role">
   <info>
      <keywordset role="hub">
         <keyword role="source-basename">hello_world</keyword>
         <keyword role="source-dir-uri">file:/home/ytrividic/Desktop/repos/idml-pandoc-reader/hello_world.idml.tmp/</keyword>
         <keyword role="archive-dir-uri">file:/home/ytrividic/Desktop/repos/idml-pandoc-reader/</keyword>
         <keyword role="source-paths">false</keyword>
         <keyword role="used-rules-only">true</keyword>
         <keyword role="formatting-deviations-only">true</keyword>
         <keyword role="source-type">idml</keyword>
         <keyword role="toc-title">Table des matières</keyword>
         <keyword role="chapter-number">1</keyword>
         <keyword role="type-area-width">523.2755905509999</keyword>
         <keyword role="footnote-restart">false</keyword>
         <keyword role="endnote-restart">false</keyword>
         <keyword role="tags-list">Root</keyword>
      </keywordset>
      <css:rules>
         <css:rule name="NormalParagraphStyle"
                   native-name="$ID/NormalParagraphStyle"
                   layout-type="para"
                   css:color="device-cmyk(0,0,0,1)"
                   css:font-weight="normal"
                   css:font-style="normal"
                   css:font-size="12pt"
                   css:letter-spacing="0em"
                   css:text-transform="none"
                   css:margin-left="0pt"
                   css:margin-right="0pt"
                   css:text-indent="0pt"
                   xml:lang="fr-FR"
                   css:hyphens="auto"
                   css:margin-top="0pt"
                   css:margin-bottom="0pt"
                   css:text-decoration-line="none"
                   css:page-break-before="auto"
                   css:text-align="left"
                   css:direction="ltr"
                   css:font-family="Minion Pro"/>
         <css:rule name="No_character_style"
                   native-name="$ID/[No character style]"
                   layout-type="inline"/>
      </css:rules>
   </info>
   <para role="NormalParagraphStyle">
      <phrase css:font-family="Arial">Hello world!</phrase>
   </para>
</hub>
```

La conversion vers DocBook par la méthode `hubxml2docbook` donne :

```xml
<?xml version="1.0" encoding="utf-8"?>
<article version="5.0" xml:lang="fr-FR" xmlns="http://docbook.org/ns/docbook">
 <para role="NormalParagraphStyle">
  <phrase>
   Hello world!
  </phrase>
 </para>
</article>
```

Et ce résultat peut être donné à Pandoc. Son AST est le suivant :

```
[ Div
    ( ""
    , []
    , [ ( "wrapper" , "1" )
      , ( "role" , "NormalParagraphStyle" )
      ]
    )
    [ Para [ Str "Hello" , Space , Str "world!" ] ]
]
```

En transformant l'attribut `role` par une classe via un filtre Lua, on obtient :

```
[ Div
    ( ""
    , [ "NormalParagraphStyle" ]
    , [ ( "wrapper" , "1" ) ]
    )
    [ Para [ Str "Hello" , Space , Str "world!" ] ]
]
```

Et ainsi le résultat final :

```markdown
::: {.NormalParagraphStyle wrapper="1"}
Hello world!
:::
```