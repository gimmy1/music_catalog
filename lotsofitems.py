from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem, User

# engine = create_engine('sqlite:///itemcatalog.db')
engine = create_engine('sqlite:///itemcatalogwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
user1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(user1)
session.commit()

# Add Category, and then add multiple CategoryItem
# First Category
category1 = Category(name="Strings", user_id=1)
session.add(category1)
session.commit()

item1 = CategoryItem(name="Violin", user_id=1, description="Violin, family of stringed musical instruments having wooden bodies whose backs and fronts are slightly convex, the fronts pierced by two-shaped resonance holes. The instruments of the violin family have been the dominant bowed instruments because of their versatility, brilliance, and balance of tone, and their wide dynamic range. A variety of sounds may be produced, e.g., by different types of bowing or by plucking the string (see pizzicato). The violin has always been the most important member of the family, from the beginning being the principal orchestral instrument and holding an equivalent position in chamber music and as a solo instrument. The technique of the violin was developed much earlier than that of the viola or cello.", category=category1)
session.add(item1)
session.commit()


item2 = CategoryItem(name="Viola", user_id=1, description="The viola is the alto instrument of the violin family (violin, viola, cello). It is constructed using the same components as the violin, the only difference being the larger size. ... In other words, the viola is too small in proportion to its tuning and this is the reason for its distinctive timbre.", category=category1)
session.add(item2)
session.commit()

item3 = CategoryItem(name="Cello", user_id=1, description="The cello is used as a solo musical instrument, as well as in chamber music ensembles, string orchestras, as a member of the string section of symphony orchestras, and some rock bands. It is the second-largest bowed string instrument in the modern symphony orchestra, the double bass being the largest.", category=category1)
session.add(item3)
session.commit()


item4 = CategoryItem(name="Banjo", user_id=1, description="The banjo is a four-, five- or six-stringed instrument with a thin membrane stretched over a frame or cavity as a resonator, called the head. The membrane, or head, is typically made of plastic, although animal skin is still occasionally but rarely used, and the frame is typically circular. Early forms of the instrument were fashioned by Africans in America, adapted from African instruments of similar design.", category=category1)
session.add(item4)
session.commit()

item5 = CategoryItem(name="Guitar", user_id=1, description="The guitar is a musical instrument classified as a fretted string instrument with anywhere from four to 18 strings, usually having six.The sound is projected either acoustically, using a hollow wooden or plastic and wood box (for an acoustic guitar), or through electrical amplifier and a speaker (for an electric guitar). It is typically played by strumming or plucking the strings with the fingers, thumb or fingernails of the right hand or with a pick while fretting (or pressing against the frets) the strings with the fingers of the left hand.", category=category1)
session.add(item5)
session.commit()


# Second Category
category2 = Category(name="Woodwinds", user_id=1)
session.add(category2)
session.commit()

item1 = CategoryItem(name="Flute", user_id=1, description="The flute is a family of musical instruments in the woodwind group. Unlike woodwind instruments with reeds, a flute is an aerophone or reedless wind instrument that produces its sound from the flow of air across an opening. Flutes are the earliest extant musical instruments, as paleolithic instruments with hand-bored holes have been found.", category=category2)
session.add(item1)
session.commit()

item2 = CategoryItem(name="Clarinet", user_id=1, description="The clarinet is a musical-instrument family belonging to the group known as the woodwind instruments. It has a single-reed mouthpiece, a straight cylindrical tube with an almost cylindrical bore, and a flared bell. It would seem however that its real roots are to be found amongst some of the various names for trumpets used around the renaissance and baroque eras.", category=category2)
session.add(item2)
session.commit()

item3 = CategoryItem(name="Saxophone", user_id=1, description="The saxophone is a family of woodwind instruments. Saxophones are usually made of brass and played with a single-reed mouthpiece similar to that of the clarinet. The saxophone family was invented by the Belgian instrument maker Adolphe Sax in 1840.", category=category2)
session.add(item3)
session.commit()

item4 = CategoryItem(name="Bassoon", user_id=1, description="The bassoon is a woodwind instrument in the double reed family that typically plays music written in the bass and tenor clefs, and occasionally the treble. Appearing in its modern form in the 19th century, the bassoon figures prominently in orchestral, concert band, and chamber music literature. The bassoon is a non-transposing instrument known for its distinctive tone colour, wide range, variety of character and agility. Listeners often compare its warm, dark, reedy timbre to that of a male baritone voice.", category=category2)
session.add(item4)
session.commit()

# Third Category
category3 = Category(name="Percussion", user_id=1,)
session.add(category3)
session.commit()

item1 = CategoryItem(name="Alfaia", user_id=1, description="The alfaia is a Brazilian membranophone. It is a wooden drum made of animal skin tensioned or loosened through ropes placed alongside the body of the instrument. Alfaias are usually between 16 and 22 inches in diameter.", category=category3)
session.add(item1)
session.commit()

item2 = CategoryItem(name="Djembe", user_id=1, description="A djembe or jembe is a rope-tuned skin-covered goblet drum played with bare hands, originally from West Africa. According to the Bambara people in Mali, the name of the djembe comes from the saying 'Anke dje, anke be' which translates to 'everyone gather together in peace' and defines the drums purpose. In the Bambara language, 'dje'' is the verb for gather and 'be' translates as 'peace'.", category=category3)
session.add(item2)
session.commit()

item3 = CategoryItem(name="Dunun", user_id=1, description="Dunun (also spelled dundun or doundoun) is the generic name for a family of West African drums that have developed alongside the djembe (also spelled dundun or doundoun) is the generic name for a family of West African drums that have developed alongside the djembe. Traditionally, the drum is played horizontally (placed on a stand or worn with a shoulder strap). For a right-handed player, the right hand plays the skin and the left hand optionally plays a bell that may be mounted on top of the drum or held in the left hand. The latter style is popular in Mali and originally from the Khassonke people.", category=category3)
session.add(item3)
session.commit()

item4 = CategoryItem(name="Ganza", user_id=1, description="The ganza is a Brazilian rattle used as a percussion instrument, especially in samba music. The ganza is cylindrically shaped, and can be either a hand-woven basket or a metal canister which is filled with beads, metal balls, pebbles, or other similar items. Those made from metal produce a particularly loud sound. They are usually used to play a rhythm underneath the rest of the band.", category=category3)
session.add(item4)
session.commit()

# Fourth Category
category4 = Category(name="Brass", user_id=1)
session.add(category4)
session.commit()

item1 = CategoryItem(name="Trumpet", user_id=1, description="A trumpet is a musical instrument commonly used in classical and jazz ensembles. The trumpet group contains the instruments with the highest register in the brass family. Trumpet-like instruments have historically been used as signaling devices in battle or hunting, with examples dating back to at least 1500 BC; they began to be used as musical instruments only in the late 14th or early 15th century.", category=category4)
session.add(item1)
session.commit()

item2 = CategoryItem(name="Tuba", user_id=1, description="The tubas the largest and lowest-pitched musical instrument in the brass family. Like all brass instruments, sound is produced by moving air past the lips, causing them to vibrate or 'buzz' into a large cupped mouthpiece. It first appeared in the mid 19th-century, making it one of the newer instruments in the modern orchestra and concert band. The tuba largely replaced the ophicleide.", category=category4)
session.add(item2)
session.commit()

item3 = CategoryItem(name="Trombone", user_id=1, description="The trombone is a musical instrument in the brass family. Like all brass instruments, sound is produced when the player's vibrating lips (embouchure) cause the air column inside the instrument to vibrate.  Many modern trombone models also utilize a rotary valve as a means to lower pitch of the instrument. Variants such as the valve trombone and superbone have three valves like those on the trumpet.", category=category4)
session.add(item3)
session.commit()

item4 = CategoryItem(name="Vienna horn", user_id=1, description="The Vienna horn s a type of musical horn used primarily in Vienna, Austria, for playing orchestral or classical music. It is used throughout Vienna, including the Vienna Philharmonic and Wiener Staatsoper.During the nineteenth century, a number of experiments were made in adding valves to the natural horn to enable it to play chromatically without the need for hand-stopping. These experiments included adding piston valves (as used in modern trumpets) to a single F horn.", category=category4)
session.add(item4)
session.commit()

category5 = Category(name="Keyboard", user_id=1)
session.add(category5)
session.commit()

item1 = CategoryItem(name="Accordion", user_id=1, description="Accordions  are a family of box-shaped musical instruments of the bellows-driven free-reed aerophone type, colloquially referred to as a squeezebox. . These vibrate to produce sound inside the body. Valves on opposing reeds of each note are used to make the instrument's reeds sound louder without air leaking from each reed block.", category=category5)
session.add(item1)
session.commit()

item2 = CategoryItem(name="Synthesizer", user_id=1, description="A synthesizer is an electronic musical instrument that generates electric signals that are converted to sound through instrument amplifiers and loudspeakers or headphones. Synthesizers use various methods to generate electronic signals (sounds). Among the most popular waveform synthesis techniques are subtractive synthesis, additive synthesis, wavetable synthesis, frequency modulation synthesis, phase distortion synthesis, physical modeling synthesis and sample-based synthesis.", category=category5)
session.add(item2)
session.commit()

item3 = CategoryItem(name="Pipe Organ", user_id=1, description="The pipe organ is a musical instrument that produces sound by driving pressurized air (called wind) through organ pipes selected via a keyboard. Because each pipe produces a single pitch, the pipes are provided in sets called ranks, each of which has a common timbre and volume throughout the keyboard compass. Most organs have multiple ranks of pipes of differing timbre, pitch, and volume that the player can employ singly or in combination through the use of controls called stops.", category=category5)
session.add(item3)
session.commit()

item4 = CategoryItem(name="Regal", user_id=1, description="The regal was a small portable organ, furnished with beating reeds and having two bellows. The instrument enjoyed its greatest popularity during the Renaissance. The name was also sometimes given to the reed stops of a pipe organ, and more especially the vox humana stop.", category=category5)
session.add(item4)
session.commit()

item5 = CategoryItem(name="Carillon", user_id=1, description="A carillon is a musical instrument that is typically housed in the bell tower (belfry) of a church or municipal building. The instrument consists of at least 23 cast bronze, cup-shaped bells, which are played serially to produce a melody, or sounded together to play a chord. A traditional manual carillon is played by striking a keyboard the stick like keys of which are called batons with the fists, and by pressing the keys of a pedal keyboard with the feet. The keys mechanically activate levers and wires that connect to metal clappers that strike the inside of the bells, allowing the performer on the bells, varies the intensity of the note according to the force applied to the key.", category=category5)
session.add(item5)
session.commit()

print "added all items!"
