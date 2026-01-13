# The Optimal Pitch of the Car Honk

*Analyzing horn frequencies across 68 vehicles from 10 manufacturers*

Welcome back to Better Know a Dataset! Today we're exploring a dataset that, until last week, didn't exist: the fundamental frequencies of car horns by make and model.

I was standing at a Manhattan intersection when three cars honked simultaneously. One was a sharp, insistent beep. Another a lower, more authoritative blare. The third somewhere in between. Together they formed something like a chord, though not a pleasant one.

This got me wondering: who decides what pitch a car horn should be? Is there a standard? And if everyone's honking at once, shouldn't someone be coordinating?

## The Regulatory Landscape

You might assume car horn frequencies are tightly regulated. They're not.

In Europe, [UNECE Regulation 28](https://unece.org/fileadmin/DAM/trans/main/wp29/wp29regs/2018/R028am5e.pdf) specifies that horns must emit 105-118 decibels at two meters, with acoustic energy concentrated in the 1500-3550 Hz range. That upper bound matters: it's roughly the frequency of a human scream, which makes evolutionary sense. We're wired to notice sounds in that range.

In the US, the standard is remarkably lax. NHTSA doesn't even require cars to have horns. If one is installed, [FMVSS 571.101](https://www.law.cornell.edu/cfr/text/49/571.101) says only that it must be "operable by the driver." No frequency mandate whatsoever.

One convention that has persisted: bigger vehicles get lower horns. According to [Wikipedia's entry on vehicle horns](https://en.wikipedia.org/wiki/Vehicle_horn), "larger cars were always equipped with horns that gave an overall lower frequency honk, and small car horns were biased toward the higher frequencies. Hence the 'beep-beep' of Volkswagens and the French-horn type sounds from Cadillacs." Some countries even mandated this relationship, with the idea that a high-pitched horn indicates a small vehicle and a lower note signals a larger one. Ships follow the same convention: the RMS Queen Mary used 55 Hz horns, low enough to travel far without being painful to passengers, and modern maritime law requires ships over 660 feet to use frequencies between 70-200 Hz.

## The Psychoacoustics of Annoyance

Before diving into the data, some theory. Why do some horns sound "better" than others?

Most modern car horns hover around 440 Hz, which is A4, the note orchestras tune to. This isn't coincidence. It's a frequency humans perceive easily across ambient noise.

Premium vehicles typically use dual horns, each at a different pitch, often a minor third apart (say, 500 Hz and 420 Hz). Why a minor third? The physics of perception. When two pure tones are close in frequency, they create "beating," a wobbling interference pattern the ear perceives as roughness. Space them a minor third apart and the roughness disappears. The chord sounds smooth. In my data, the four vehicles with detectable dual horns all used consonant intervals: the Chevrolet Tahoe pairs 538 Hz with 657 Hz (a minor third), while the Nissan Pathfinder uses 431 Hz and 323 Hz (a perfect fourth). No manufacturer paired horns a semitone apart, which would create maximum dissonance.

This preference for consonance turns out to be universal. A [2024 study in Nature Communications](https://www.nature.com/articles/s41467-024-45812-z) tested perception of musical intervals in communities including the Tsimane' of the Bolivian Amazon and villagers in Papua New Guinea with minimal exposure to Western harmony. Everyone found rough intervals unpleasant. The aversion to acoustic beating isn't cultural. It's wired in.

So car manufacturers have independently converged on similar solutions: frequencies around 400-500 Hz, often in consonant pairs, loud enough to cut through traffic but not so harsh as to be unbearable.

At least, that's the theory. I wanted to see what's actually happening on the road.

## Building the Dataset

I went looking for a comprehensive database of car horn frequencies by make and model. It doesn't exist. Car enthusiasts on forums share scattered measurements. Some manufacturers publish specs, but most don't. The regulation is minimal, so there's no compliance database.

So I built one.

**Methodology**: I searched YouTube for horn sound tests for 95 vehicles across 10 manufacturers (Toyota, Ford, Chevrolet, Honda, Hyundai, Nissan, Kia, BMW, Mercedes-Benz, and Tesla). For each video, I extracted the audio, isolated the horn segment, and ran a Fast Fourier Transform to identify the fundamental frequency. The analysis pipeline used Python's `librosa` library with a 4096-sample FFT window, identifying peaks in the 200-800 Hz range most likely to represent the horn's fundamental.

**Caveats**: YouTube audio compression isn't ideal for acoustic analysis. Some videos included ambient noise or reverb that could shift the detected fundamental. I excluded samples where the spectral peak was ambiguous or fell outside the plausible 150-850 Hz range. The final dataset includes 68 vehicles where I had high confidence in the frequency measurement.

The full dataset and analysis code are available on [GitHub](https://github.com/sangmino/car-honks).

**What do these horns actually sound like?** Here are a few samples from the dataset:

🔊 **BMW 3 Series** (398 Hz): [samples/bmw_3_series_2023.wav](samples/bmw_3_series_2023.wav)
🔊 **Toyota Camry** (484 Hz): [samples/toyota_camry_2023.wav](samples/toyota_camry_2023.wav)
🔊 **Chevrolet Corvette** (770 Hz): [samples/chevrolet_corvette_2023.wav](samples/chevrolet_corvette_2023.wav)

## The Results

Here's what 68 car horns look like.

### The Full Distribution

![Car horn frequencies by manufacturer](figures/fig1_individual.png)

Each dot represents one vehicle. Manufacturers are ordered by mean frequency, with horizontal lines showing the average for each brand. Most vehicles cluster in the 400-500 Hz range (shaded), but the outliers are dramatic. The Corvette screams at 770 Hz (roughly G5), while the Mercedes-Benz A-Class murmurs at 242 Hz.

Mercedes-Benz sits at the bottom with a mean of 328 Hz. Kia at the top with 515 Hz. BMW lands at 431 Hz, almost exactly on concert pitch (A4 = 440 Hz).

The spread within manufacturers is interesting too. Ford's tight 50 Hz spread implies a standardized approach across their lineup. Tesla shows the widest variation at 220 Hz, ranging from the Model 3/Y at 253 Hz to the Cybertruck at 770 Hz.

### By Country of Origin

![Horn frequency by country of origin](figures/fig2_country.png)

German luxury brands (BMW, Mercedes-Benz) cluster around 384 Hz on average, while American manufacturers (Ford, Chevrolet, Tesla) run about 76 Hz higher at 460 Hz. In musical terms, that's roughly a major second, the interval between "do" and "re."

Japanese manufacturers land in the middle at 453 Hz, close to concert pitch (A4 = 440 Hz). Korean manufacturers (Hyundai, Kia) cluster slightly higher at 498 Hz.

### The Luxury Gap

![Luxury vs mass market horn frequencies](figures/fig3_luxury.png)

Perhaps the most striking finding: luxury vehicles (BMW, Mercedes-Benz) average 384 Hz. Mass market vehicles average 467 Hz. That 83 Hz gap is roughly a minor second, the most dissonant interval in music.

The Mercedes-Benz announces itself with a baritone authority; the Kia Forte chirps from the tenor section. This pattern holds even within manufacturer: the BMW X5 (luxury SUV) honks lower than the Honda Civic (mass market compact), confirming that the "big car, low pitch" convention documented in the Wikipedia article extends to modern vehicles.

## The Economics of Honking

Here's where this gets interesting from a social science perspective.

Traffic noise isn't just annoying. It's expensive. A [recent NBER paper](https://www.nber.org/papers/w34298) by Currie, Davis, Greenstone, and Walker estimates the aggregate cost of traffic noise in the US at **$110 billion annually**. To be clear: this paper studies general traffic noise (engine sounds, tire noise, etc.), not horns specifically. But the methodology is instructive.

The authors use a clever identification strategy. When states build noise barriers along highways, property values in the newly quieted areas rise. By comparing prices before and after barrier construction, they estimate that each decibel of noise reduction is worth about 0.4-1.1% in property values. Extrapolating across all US properties near major roads gives the $110 billion figure.

The costs are not evenly distributed. The burden falls disproportionately on low-income and minority households, making traffic noise a **regressive externality**—a cost imposed on others that hits poorer people harder. The authors calculate that internalizing these costs would require a **Pigovian tax** (a tax designed to correct for negative externalities) of $974 per vehicle.

One finding particularly relevant to our topic: the shift to electric vehicles, which are quieter than internal combustion engines at low speeds, could yield **$77 billion in noise reduction benefits**, about a fifth of EVs' total external benefit. This raises an interesting question: do EVs also have different horn frequencies?

### Do EVs Sound Different?

With 11 electric vehicles in my sample (including Tesla's lineup, BMW i4, Hyundai Ioniq 5/6, Kia EV6, Chevrolet Bolt, and Nissan Ariya), I can now answer this question directly.

![EV vs ICE horn frequencies](figures/fig4_ev_ice.png)

The answer: not really. EVs average 459 Hz versus 450 Hz for internal combustion vehicles, a difference of just 9 Hz, well within the noise. The surprise is the Cybertruck at 770 Hz, matching the Corvette as the highest horn in the dataset. Tesla's other vehicles cluster around 253-554 Hz, right in the mainstream range.

This makes sense. Horn frequency is a design choice constrained by physical size and cost, not propulsion type. An EV still needs the same audible warning as a gas car, and there's no particular reason a battery pack would change the calculus. The one exception might be very compact EVs where packaging constraints favor smaller, higher-pitched horns, but Tesla's lineup doesn't show this pattern.

Horns are a small piece of the noise picture, but they're a pointed one. A horn is *deliberately* annoying. That's the point.

## The Social Planner's Problem

Economists have a useful thought experiment called the **social planner**. Imagine a benevolent, all-knowing decision-maker whose only goal is to maximize total welfare for society. No politics, no lobbying, no corporate interests. Just: what arrangement would make everyone best off?

The social planner is fictional, of course. But the concept helps us spot when individual decisions add up to collective problems.

Here's the puzzle with car horns. Each manufacturer chooses a horn pitch to maximize the probability that their customers' honks get noticed, subject to not being so grating that buyers complain. Toyota optimizes for Toyota. Honda optimizes for Honda. Everyone's doing what's best for themselves.

But when multiple cars honk at once, all that individual optimization creates a collective mess. The resulting cacophony is worse than the sum of its parts. Two horns a semitone apart create beating. Three random pitches create chaos. What's good for each company isn't good for everyone standing at the intersection.

Economists call this a **coordination failure**. Each player is acting rationally, but the outcome is worse than if they'd coordinated. It's the same logic behind traffic jams (everyone takes the "fastest" route, which makes it slow), overfishing (each boat maximizes its catch, depleting the stock), and, apparently, Manhattan soundscapes.

So what would a social planner do with car horns? She might assign frequencies to manufacturers to ensure harmony. Toyota gets 440 Hz. Honda gets 523 Hz (a major third up). BMW gets 659 Hz (a perfect fifth). Now when all three honk at once, they form a major chord. The intersection becomes a symphony.

This isn't as crazy as it sounds. We already do this for radio frequencies: the FCC assigns spectrum so stations don't interfere with each other. Musicians worldwide agreed that A=440 Hz so orchestras can tune together. Why not horns?

There's a counterargument, of course: chaos might be the point. Random pitches are more attention-grabbing than harmonious ones. If the goal is to alert pedestrians to danger, maybe we want horns that *don't* blend into a pleasant hum. The semitone clash that sounds terrible at the intersection might be saving lives. And if luxury cars use distinctively low pitches, and pedestrians learn to associate low honks with expensive (and presumably faster) vehicles, that's useful information too. A coordinated system might preserve safety while destroying the signal.

## If You're Starting a Car Company

Say you're launching a new electric vehicle brand and need to choose a horn frequency. What should you pick?

Based on the data, you have three main strategies:

**1. Join the cluster (400-500 Hz)**

Most manufacturers land here. Your horn blends with traffic—safe, unremarkable, unlikely to annoy customers or stand out. This is the Toyota/Honda approach: reliable, inoffensive, forgettable.

**2. Go low (300-350 Hz)**

This is the BMW/Mercedes strategy. A lower pitch sounds more authoritative and signals "large vehicle approaching" even if you're selling a compact. It also differentiates your brand acoustically. The downside: lower frequencies require larger horn assemblies, which cost more and take up space.

**3. Go high (600+ Hz)**

The Corvette approach. Maximum attention-grabbing, maximum annoyance. Your customers will definitely be heard. Everyone else will hate them. This works for sports cars where aggression is part of the brand identity, but probably not for a family SUV.

**4. Coordinate for consonance (the road not taken)**

If you knew every other manufacturer's frequency, you could pick a pitch that forms pleasant intervals with the most common horns. At 430 Hz and 500 Hz (the two densest clusters), adding a horn at 344 Hz would create a major triad with any car in those ranges. Adding one at 645 Hz would create a major seventh chord.

Nobody does option 4. Each manufacturer optimizes alone, and the intersection symphony remains unwritten.

## Takeaways and Future Research

**What we learned:**

1. **Car horn frequencies vary widely** (242-770 Hz in my sample), with no regulatory standardization in the US.

2. **The "big car, low pitch" convention persists**: German luxury brands average 384 Hz vs. 460 Hz for American manufacturers.

3. **The luxury gap is real**: An 83 Hz difference separates luxury from mass-market vehicles.

4. **Dual horns use consonant intervals**: Manufacturers avoid dissonant pairings, consistent with universal preferences documented in psychoacoustics research.

5. **Traffic noise imposes $110 billion in annual costs**, and EVs could capture $77 billion of that as a noise reduction benefit.

6. **EVs don't sound different**: With 11 EVs in the sample, there's no systematic difference in horn frequency between electric and internal combustion vehicles.

**Questions for future research:**

1. **Correlate with MSRP**: Does horn frequency predict vehicle price? A proper regression with price data would nail it down.

2. **Record actual intersections**: What does the frequency distribution look like at a real Manhattan intersection? What chords emerge naturally?

3. **Test pedestrian response**: Do people actually react differently to 350 Hz versus 500 Hz horns? Is the "low pitch = big vehicle" signal actually received?

4. **International comparison**: Are horn frequencies different in Seoul versus Stuttgart versus Detroit? Does local taste influence design?

The data now exists. The coordination problem remains unsolved. And somewhere in Manhattan, three cars are honking a diminished chord, and nobody's enjoying it.

---

*The dataset and analysis code are available on [GitHub](https://github.com/sangmino/car-honks). If you extend this analysis, I'd love to hear about it.*
