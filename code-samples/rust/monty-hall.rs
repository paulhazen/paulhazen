use rand::{rngs::ThreadRng, Rng};

const GOAT:u8 = 0;
const CAR:u8 = 1;
const DOOR_COUNT:f32 = 3.;

fn main() {
  // todo: Move the following variables to be arguments
  let mut rng = rand::thread_rng();
  let runs = 100000;

  // indicate simulations being run
  println!("{} simulations of monty-hall are running", runs);

  // run simulations of monty-hall where player switches doors after reveal
  let switch_doors = run_simulations(&mut rng, true, runs);

  // run simulations of mont-hall where player keeps their guess
  let keep_door = run_simulations(&mut rng, false, runs);

  // print the rates at which prizes are won depending on strategy.
  println!("Switch doors: {}", switch_doors);
  println!("Keep door: {}", keep_door);
}

// run a series of simulations
fn run_simulations(rng: &mut ThreadRng, switch_doors:bool, simulation_runs: usize) -> f32 {
  let mut correct_guesses = 0;
  for _ in 0..simulation_runs {
    if true == run_simulation(rng, switch_doors) {
      correct_guesses += 1;
    }
  }

  correct_guesses as f32 / simulation_runs as f32
}

// run a single simulation
fn run_simulation(rng:&mut ThreadRng, switch_doors:bool) -> bool {
  // create the doors, and randomly set one of them to be the prize
  let mut doors = vec![GOAT;DOOR_COUNT as usize];
  
  //doors[rng.gen_range::<usize>(0, 3)] = CAR;
  doors[rng.gen_range(0..3)] = CAR;


  // player makes a guess
  let mut guess_index = rng.gen_range(0..3);

  // if we are switching doors, then we have some more work to do
  if switch_doors {
    // since we are allowed to switch doors, we will open one door with a goat
    // behind it that is *not* the one we already guessed, then we will change
    // our guess index to the other door remaining
    let mut opened_index = rng.gen_range(0..3);
    loop {
      if doors[opened_index] == GOAT && guess_index != opened_index {
        break;
      } else {
        opened_index = rng.gen_range(0..3);
      }
    }
    // by definition, we switch our guess index to be the one that is
    // not our current guess, nor the opened index
    for i in 0..3 {
      if i != opened_index && i != guess_index {
        guess_index = i;
        break;
      }
    }
  }

  CAR == doors[guess_index]
}