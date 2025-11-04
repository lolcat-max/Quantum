
# Interleaving high‑Z plates with scintillator or silicon pads for charge producing device from gamma rays

If an atom “accepts” a positron but not an electron, the distinctive energy it releases is annihilation radiation: typically two back-to-back gamma rays at 511 keV each from electron–positron annihilation, or a 3‑gamma decay if positronium forms in the triplet state.
[](https://x.com/GeorgeW479744)
An electron linac sends ~5–100 MeV electrons into a tungsten converter; bremsstrahlung photons inside the target convert to e+e− pairs, and a dipole magnet separates and transports the positron beam for moderation and use.

Interleaving high‑Z plates with scintillator or silicon pads yields an efficient, charge‑producing detector for gamma rays across 511 keV to multi‑GeV: the high‑Z absorber converts photons via Compton/pair production, and the active layers collect charge or light from the ensuing electromagnetic shower for precise timing, imaging, and energy measurement.[^1][^2]

### Abstract

- Objective: Design a modular converter–sampler that detects both 511 keV annihilation photons from e+e− interactions and GeV‑scale gammas from linac‑bremsstrahlung, providing >50% conversion in a compact form and scalable readout for spectroscopy and imaging.[^3][^4]
- Approach: Alternate tungsten plates of order 1 radiation length X0 with silicon pad planes or scintillator tiles; at 511 keV the device functions as a high‑efficiency coincidence spectrometer, while at GeV energies it acts as a compact electromagnetic calorimeter for shower capture.[^2][^5]


### Physics basis

- Conversion: At ≥100 MeV, pair production dominates; a stack of 6–8 X0 achieves >50% interaction probability, while 20–30 X0 contains most of the shower for accurate energy sums; tungsten’s X0≈3.5 mm enables compact layers.[^6][^2]
- 511 keV regime: Detection relies on photoelectric/Compton interactions in dense scintillators or converters with high solid angle and fast coincidence timing to tag back‑to‑back annihilation photons, as in PET‑style systems.[^7][^3]


### Detector architecture

- Absorber: Tungsten plates, 3.5 mm each (≈1 X0), purity ≥99.9%, stacked for total depth 18–24 X0 depending on target energy; small Molière radius (~9 mm) improves shower compactness and two‑photon separation.[^8][^2]
- Active layers:
    - Silicon pads: 300 µm n‑type FZ wafers diced into 1×1 cm pads on each plane; reverse‑biased to collect e–h pairs from shower secondaries with pad‑level imaging and summing for energy.[^9][^1]
    - Scintillator tiles: Alternatively, plastic or crystal tiles (e.g., LYSO, PbWO4) coupled to SiPM arrays for higher light yield and fast timing; LYSO improves 511 keV efficiency and spatial resolution relative to NaI(Tl) modules.[^10][^7]


### Readout and electronics

- Front‑end: Low‑noise charge‑sensitive preamplifiers on silicon pads or SiPM transimpedance stages on scintillators; per‑layer digitizers sample amplitude and time for clustering and longitudinal shower profiling.[^1][^2]
- Trigger: Two‑level logic—coincidence timing windows of a few ns for 511 keV pairs; energy‑sum and topological triggers for GeV showers, with optional preshower pixel layers near shower maximum to resolve close photon pairs.[^9][^3]


### Performance targets

- 511 keV: Coincidence detection with high efficiency and improved angular resolution using small‑pitch LYSO or finely segmented silicon planes; true/scatter/random classification follows PET practice with tight timing windows.[^3][^7]
- GeV gammas: Sampling resolution scales roughly as a/√E ⊕ b; silicon–tungsten prototypes with 18–20 X0 and cm‑scale pads demonstrate accurate shower centroids and energy sums suitable for π0/η photon reconstruction and compact calorimetry.[^5][^1]


### Applications

- Positron annihilation studies: Line‑of‑response imaging and lifetime/ACAR‑style coincidence leveraging 511 keV back‑to‑back gammas; high‑granularity readout supports materials and detector R\&D.[^7][^3]
- Linac and bremsstrahlung beams: Diagnostic calorimetry for 5–100 MeV electron linacs with tungsten converters; monitor spectra, dose, and alignment while supporting positron‑source development downstream of the converter.[^4][^11]


### >50% conversion and containment

- Front converter: A 6–8 X0 tungsten front‑end layer in front of silicon tracking planes ensures >50% conversion to e+e− at GeV energies, enabling direction reconstruction before the main calorimeter.[^2][^5]
- Full stack: A 20–30 X0 silicon–tungsten sampling calorimeter achieves high detection efficiency and energy containment for compact GeV detection; layer counts and pad sizes are tuned to Molière radius and readout cost.[^12][^2]


### Integration with positron sources

- An electron linac impinging on a tungsten target produces bremsstrahlung; those photons create e+e− pairs within the converter; dipole optics separate positrons for moderation/trapping, while a downstream calorimeter stack characterizes the photon field and shower properties.[^13][^11]
- Energy‑recovery linac concepts spatially separate the bremsstrahlung radiator from isotope/positron targets, improving photon yield and efficiency—compatible with using the calorimeter as an inline diagnostic.[^14][^11]


### Example prototypes and references

- Silicon–tungsten calorimeters with 19–30 alternating layers have been built and beam‑tested, using 3.5 mm W plates and 300 µm silicon pads, demonstrating granular shower imaging and robust energy measurement in compact geometries.[^1][^2]
- FoCal‑E and similar pad/pixel silicon–tungsten designs document absorber thickness, pad sizes, and readout schemes, providing templates for modular buildouts and preshower integration.[^12][^9]
<span style="display:none">[^15][^16][^17][^18][^19][^20][^21]</span>

<div align="center">⁂</div>

[^1]: https://cds.cern.ch/record/2702130/files/Muhuri_2020_J._Inst._15_P03015.pdf

[^2]: https://www.hep.ph.ic.ac.uk/calice/conferences/040329calor04/CALICE-ECAL-CALOR04.pdf

[^3]: https://pmc.ncbi.nlm.nih.gov/articles/PMC2891023/

[^4]: https://upcommons.upc.edu/bitstream/handle/2099.1/10297/pfc_cristian_garrido_MEMORIA.pdf?isAllowed=y\&sequence=1

[^5]: https://inspirehep.net/files/1ab3367bcf5c93f00ed3d4566c094c30

[^6]: https://en.wikipedia.org/wiki/Radiation_length

[^7]: https://arxiv.org/html/2412.16024v1

[^8]: https://www.fzu.cz/~cvach/CvachJ_ccsp2008.pdf

[^9]: https://arxiv.org/pdf/1912.11115.pdf

[^10]: https://en.wikipedia.org/wiki/Scintillation_counter

[^11]: http://accelconf.web.cern.ch/P05/PAPERS/RPAP036.PDF

[^12]: https://arxiv.org/pdf/2306.06153.pdf

[^13]: http://www.arxiv.org/pdf/2006.05966.pdf

[^14]: https://patents.google.com/patent/US20170076830A1/en

[^15]: https://www.sciencedirect.com/science/article/abs/pii/S0168900214008614

[^16]: https://www.sciencedirect.com/science/article/abs/pii/S0969806X97002776

[^17]: https://indico.ihep.ac.cn/event/8706/contributions/103655/attachments/55444/63779/CEPC-CDR-review-ECAL.pdf

[^18]: https://www.sciencedirect.com/science/article/abs/pii/S0969804325002155

[^19]: https://www.sciencedirect.com/science/article/abs/pii/S0168900219313038

[^20]: https://linac96.web.cern.ch/proceedings/tuesday/tu301/Paper.pdf

[^21]: https://escholarship.org/content/qt1244t3h7/qt1244t3h7.pdf

