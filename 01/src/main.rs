use anyhow::{bail, Result};
use std::fs::File;
use std::io::{prelude::*, BufReader};
use structopt::StructOpt;

fn find_pair_internal(numbers: &[u32], target: u32) -> Result<(u32, u32)> {
    for (i, number) in numbers.iter().enumerate() {
        for candidate in numbers[(i + 1)..numbers.len()].iter() {
            if number + candidate == target {
                return Ok((*number, *candidate));
            }
        }
    }
    bail!("No pair found matching {}", target);
}

fn find_pair(numbers: &[u32]) -> Result<u32> {
    let (a, b) = find_pair_internal(numbers, 2020)?;
    Ok(a * b)
}

fn find_triplet(numbers: &[u32]) -> Result<u32> {
    for (i, number) in numbers[0..(numbers.len() - 2)].iter().enumerate() {
        if let Ok((a, b)) = find_pair_internal(&numbers[(i + 1)..numbers.len()], 2020 - number) {
            return Ok(a * b * number);
        }
    }
    bail!("Could not find triplet totalling 2020");
}

#[derive(Debug, StructOpt)]
pub struct Flags {
    #[structopt(short = "i", long = "file")]
    pub file: String,
    #[structopt(short = "n", long = "next")]
    pub next: bool,
}

fn main() -> Result<()> {
    let flags = Flags::from_args();
    let file = File::open(flags.file)?;
    let numbers: Vec<u32> = BufReader::new(file)
        .lines()
        .map(|l| {
            l.expect("Could not read line")
                .parse()
                .expect("Could not parse number")
        })
        .collect();
    let result = if flags.next {
        find_triplet(&numbers)?
    } else {
        find_pair(&numbers)?
    };
    println!("{:?}", result);
    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::{find_pair, find_triplet};

    #[test]
    fn test_find_pair() {
        assert_eq!(
            find_pair(&vec![1721, 979, 366, 299, 675, 1456]).unwrap(),
            514579
        );
    }

    #[test]
    fn test_find_triplet() {
        assert_eq!(
            find_triplet(&vec![1721, 979, 366, 299, 675, 1456]).unwrap(),
            241861950
        );
    }
}
